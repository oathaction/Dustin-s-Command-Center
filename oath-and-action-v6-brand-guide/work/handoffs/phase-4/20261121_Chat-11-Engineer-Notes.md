# Chat 11: engineer notes

Status: 19:05 UTC. Started 18:57 UTC. Step 1's three contracts (C4, C5, C6) written at 19:05, before any build; building C4 now.

## Contracts

Chat 10's C1 (photographs), C2 (chapter 16 in the build) and C3 (the application kit) stand in `20261121_Chat-10-Engineer-Notes.md`. Each contract below says when it goes live.

### C4. Page plates in the guide: the kit's frames, their headings and their icons (register row "The article plate's headings and icon path")

Written 19:05 UTC, before the build. **Not live yet**; this section says when it is.

**How a chapter asks for an application.** A specimen file holds one placeholder where the kit's drawing goes, as a chart specimen holds `data-oa-chart`:

```html
<div data-oa-app="A05" data-oa-app-views="1440-light 390-light 390-dark"></div>
```

- `data-oa-app`: the application's id (`A04` on; the content file `work/build/app-kit/specs/a05-*.json`).
- `data-oa-app-views` (optional): which of its frames, in that order, by view key: `<width>-<theme>` (`1440-light`, `390-dark`), or `<width>-<theme>-<state>` where the spec draws states (`390-light-open`, the menu open). Left out, every frame the kit drew, in the spec's order. An unknown key is a build warning.
- `data-oa-app-title` (optional, web pages): prints the page's own `<title>`, read from the kit's plate, on a line above the frames, led by the attribute's words, for example `data-oa-app-title="Page title"` (AL-01: "copied from the page's markup by the renderer, never typed twice").
- Nothing else inside the placeholder. The specimen keeps its own words around it (a label line, a key) as any specimen does. Never copy a frame's markup into a specimen: markup carrying `data-oa-page-frame` in a specimen's own file is a build warning, so `--strict` fails.

**Where the drawing comes from.** A content file that sets `"guide": true` gets a guide plate: `node work/build/app-kit/oa-app.mjs build A05` (under the lock) draws the application and writes `work/build/app-kit/plates/a05.json`: its frames (view key, width, height, alt, markup) and `inputs`, every file the kit read to draw it with its SHA-256. The guide build puts the frames in place of the placeholder and re-hashes `inputs`; a file that changed since the kit drew the plate is a warning ("run oa-app.mjs build A05"), so a strict build never prints a stale drawing. The kit's shared style for each renderer type (`plates/<type>.css`) goes into the page once, in the head (`<style data-oa-app-kit="web-page">`), and weighs against the chapter whose section first draws that type (chapter 20 for `web-page`).

**What a frame is in the guide.** Every kit frame, a web page's or a still's (the share preview, each icon), is a picture named by its own alt, with the application's real markup inside it:

```html
<div class="oa-app-frame" data-oa-page-frame="A05 390-light" data-w="390" data-h="2412">
  <svg class="oa-app-scale" viewBox="0 0 390 2412" role="img" aria-label="(the view's alt)">
    <foreignObject x="0" y="0" width="390" height="2412">
      <div class="oa-app-art" inert aria-hidden="true" data-oa-picture> (the page: header, nav, main, h1, h2, footer) </div>
    </foreignObject>
  </svg>
</div>
```

- The frame scales to the plate's column (an SVG `viewBox`, no script), and inside it the page lays out at its own width by container queries and `cqi` type (contract C3), so a 390 px frame shows the 390 px page.
- `inert` and `aria-hidden="true"`: no Tab stop and nothing a screen reader reads inside the frame; it is heard once, by its alt. A chapter 20 plate's manifest entry sets `"readable": true`, so the stage is a group named by its label and each frame is one image inside it.
- **The working pages are the exports.** Every link, the menu button and the theme switch work in the standalone HTML pages the kit exports beside the PNGs (contract C6's list), where the accessibility lead walks them; inside the guide they are pictures.

**Headings.** A frame keeps the page's real `h1` to `h3`, since a page's outline is what chapter 20 teaches. The allowance is as narrow as "Choose a chart"'s: a heading is allowed in a specimen only inside a kit frame the build wrote, whose content is `inert` and `aria-hidden="true"`, so it never joins the guide's own outline. Anywhere else in a specimen, a heading still fails (the build's heading rule and the guide check's `specimenHeadings`); a page frame that is not inert and hidden fails the guide check's new `pageFrame` test. Links, buttons and fields inside the same frames are allowed on the same terms (the build's "image stage holds a control" warning and `specimenPicture`'s control test leave them alone because nothing can reach them).

**Icons from the guide's sprite.** Every icon a kit page draws is a `<use>` of the guide's sprite, never an inline path: a Civic Line or pillar icon as the guide's 1x and 2x pair (`<use class="oa-at-1x" href="#oa-sym-cl-031-24px"/><use class="oa-at-2x" href="#oa-sym-cl-031"/>`), a utility icon at 16 or 24 px (`href="#oa-sym-u-menu-24px"`). Chapter 18's switch is read from its own files, and the kit draws its Selected check as `<use href="#oa-sym-u-selected-check-24px"/>` in place of the file's path (the file stays as chapter 18 wrote it). In the guide the build's sprite carries each symbol once; in an export the kit writes the same symbols in a hidden sprite at the top of the page, by `tools/sprite_symbols.py`. Identity masters (wordmark, lockmark, ampersand B) are no sprite symbols and stay inlined from their files, by `lib.mark()`. Icons the sprite lacks (none known for chapter 20: the 36 utility symbols include menu, close, chevron, search, another-site, arrow and selected-check) go to "Requests" before any drawing.

**Type sizes.** The guide check's `typeScale` reads a frame's words against the type tokens as they compute at that frame's own width (a probe inside the frame), plus the floors, ceilings and chart sizes it already allows. The 13 px floor and the contrast test still read every word inside a frame (it carries `data-oa-picture`, as an image stage's picture does), at the size and colors the page sets.

**Ids.** The kit gives every id in a frame a prefix of its own (`a05-390-light-`), and the build adds the specimen's, so one plate can sit in two specimens.

### C5. Color by screen, for DR-310 (Rule 05.1 on a long page)

Written 19:05 UTC. **Not live yet.**

**What it measures.** On a page capture, Newsprint, dark (Charcoal plus Prussian) and Pillar Red shares, and the dark panels, for the page's first screen and for each section's opening screen; Rule 05.1 as DR-310 words it. A screen is the window's height at that width (the spec's `vh`: 900 at 1440, 768 at 1024, 844 at 390, 780 at 360 unless the page spec sets others).

**How a page marks its sections.** Put `data-oa-section="<short name>"` on the outer element of each section after the first screen (for example `<section data-oa-section="Track" ...>`). Its top edge starts that section's opening screen: from its top down one window's height, cut at the page's end. The first screen (0 to one window) is always measured and needs no mark. A dark panel is any element painted Charcoal or Prussian (read from the computed background, the outermost of nested ones), and it counts in the section where its top falls; the footer counts in the last.

**What it judges.** A light frame: Newsprint 60 to 85 percent, at most one dark panel per section, Pillar Red (signature red included) within 5 percent, on each measured screen. A dark frame: its shares and panels are printed, and only the red limit is judged (Rule 05.1's Newsprint share is the light view's; the dark mode is DR-204's). Pixels count as a color within 3 levels on each channel of the token (24 for red, which antialiasing spreads).

**How to run it.** The kit records each frame's sections and panels when it captures the frame, and `python3 -I work/build/app-kit/tools/export_checks.py OUT EXPORTS` prints a line per frame and screen, for example `1440 light, first screen: Newsprint 71.2, dark 14.0, red 0.3; 1 panel` with PASS or FAIL. Alone, on any capture: `python3 -I work/build/app-kit/tools/screen_shares.py CAPTURE.png --vh 900 --sections "Track:1320,Act:2980" [--theme light] [--json OUT]`.

### C6. The share preview and the favicon set as kit types

Written 19:05 UTC. **Not live yet.**

Two renderer types, sized from the website rows of `work/research/20261121_Platform-Specifications.json`, each drawn from ampersand B's masters (DR-116; Rule 04.7; Rule 08.2's row "Favicon: never the lockmark").

**`share-image`** (row `website.share_preview`, 1200 x 630 px, PNG). The link-preview card the identity proofs set (Rule 08.2's card): a kicker, a headline at the title style that may set ampersand B as its "and" in the one working red, and Rule 08.2's 96 px sign-off (the 48 px master at twice its size) in the bottom right, on Newsprint or Charcoal. Keys: `ground` (`newsprint` or `charcoal`), `kicker` [lead, tail], `headline` (lines; `{B}` marks the ampersand), `alt`, `export_name`. The export carries `og:image:width`, `og:image:height` and `og:image:alt` in the website's head (the kit's page exports print them). It passes Rule 08.2's feed test at 500 and 360 px wide, which the kit's export checks run.

**`favicon-set`** (one content file, six files):

| File | Row | Size | Drawing |
|---|---|---|---|
| SVG favicon | `website.favicon_svg` | `sizes="any"`, a 16 by 16 viewBox | B's 16 px master (14 by 16) centered on whole pixels, no tile, in signature red, as Rule 04.7's plate draws it on a light and a dark tab |
| `favicon.ico` | `website.favicon_ico` | 16, 32 and 48 px in one file (the row's studio choice) | B's 16 px master, no tile, at 1x, 2x and 3x on a clear ground, signature red |
| Apple touch icon | `website.apple_touch_icon` | 180 x 180 | The app icon: B on the Charcoal square, B 58 percent of the tile (Rule 04.7), B's display master, signature red |
| Manifest icon 192 | `website.manifest_192` | 192 x 192 | As the Apple touch icon |
| Manifest icon 512, maskable | `website.manifest_512` | 512 x 512 | The Charcoal square full bleed, B inside the row's safe circle (radius 40 percent of the width) |

The red on Charcoal holds 4.49 to 1 (Rule 04.7's reason). The no-tile favicon's ink follows Rule 04.7's plate (signature red on a light and a dark tab); the content file's `favicon_ink` key carries it, so the design director's page specs can set another. Each file's dimensions are checked by `check-dimensions.py`, which learns ICO (every size inside the file) and SVG (a square viewBox).

## Routine calls

- D4-xxx | A page plate asks for the kit's drawing by a placeholder (`<div data-oa-app="A05">`) that the guide build fills from `work/build/app-kit/plates/<id>.json`, as a chart specimen holds `data-oa-chart` | The kit needs Chromium to measure each frame's height, so it draws when `oa-app.mjs build` runs and the build only places; the placeholder keeps kit markup out of every specimen file (brief section 6.3), and the build refuses a frame copied into one
- D4-xxx | The build re-hashes every file the kit read to draw a plate and warns when one changed, so `--strict` never prints a stale drawing | The kit draws ahead of the build; a token or a component file changing after it would otherwise reach the page unseen
- D4-xxx | Every kit frame in the guide is a picture: an SVG with `role="img"` named by its alt, its markup `inert`, `aria-hidden="true"` and `data-oa-picture`; the page plate's manifest entry sets `"readable": true` | The accessibility lead's AL-18 (a keyboard reader would press Tab over a hundred times per plate otherwise); `inert` keeps every link out of the Tab order; `data-oa-picture` keeps the frame's words under the guide check's floor and contrast tests
- D4-xxx | The guide check allows a page's own headings and landmarks only inside a kit frame that is inert and hidden, and adds `pageFrame` to hold every frame to that form | "As narrow as Choose a chart's" (brief 8.1 (a)): one structure the build alone writes, with a test that fails any frame that leaks into the guide's outline
- D4-xxx | `typeScale` reads a frame's words against the type tokens computed at the frame's own width (a probe inside the frame) | The frame restates the fluid tokens in `cqi` (contract C3), so a 1,024 px frame's title is 88.6 px, a size the guide's own page never sets at 1,440
- D4-xxx | The kit's style for each renderer type sits once in the page's head and weighs in the chapter that first draws a frame of that type | Six web plates repeating the page style would add tens of kilobytes; charging it to its first chapter keeps chapter 20's figure honest
- D4-xxx | Frames named in one placeholder share one row at one scale (each grows by its true width, never past it) | A 1,440 px page and a 390 px page side by side then read in proportion; the design director gets another row by another placeholder
- D4-xxx | The kit draws chapter 18's Selected check, Menu and Close icons as `<use>` of the guide's sprite, converting the component file's inline path as it reads it (`sprite_icons()`); chapter 18's files stay as written | Register row "The article plate's headings and icon path"; the sprite holds all three (`oa-sym-u-selected-check-24px`, `-menu-24px`, `-close-24px`)
- D4-xxx | A screen for DR-310 is one window's height at the page's width (900, 768, 844 and 780 px unless a spec sets others); a dark panel is an element painted Charcoal or Prussian, the outermost of nested ones, of 3 percent of a screen or more | The window heights chat 10's sample used; a button or chip painted Charcoal is no panel
- D4-xxx | A dark page is judged on red alone under Rule 05.1; its Newsprint share is printed, not judged | Rule 05.1's Newsprint limit is the light view's; the dark mode is DR-204's
- D4-xxx | The favicon draws in signature red with no tile on light and dark tabs, from B's 16 px master centered in a 16 px square; the app icons put B at 58 percent of a full-bleed Charcoal square from the display master | Rule 04.7's text and its plate (s-04-7-correct), which draws the favicon in signature red on both tabs and the app icon at 94.84 by 104.40 px in 180
- D4-xxx | The ICO holds three PNG images (16, 32 and 48 px) the kit drew, written by `tools/ico.py` | The row's studio choice; PNG inside ICO is read by every current browser, and writing it needs no package
- D4-xxx | The exports manifest is one file for the folder: a build of some applications replaces their entries and keeps the others' | Chat 10's command rewrote the manifest with only the applications it built, which would drop A01 to A03 from `check-dimensions.py` on the next build

## Done

## Requests

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

## Not tested
