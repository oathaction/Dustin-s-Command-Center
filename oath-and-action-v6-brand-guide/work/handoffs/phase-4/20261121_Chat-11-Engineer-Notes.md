# Chat 11: engineer notes

Status: 22:38 UTC. Started 18:57 UTC. The main session's 22:07 call (the guide check inside page frames) done at 22:38 (below); craft fixes and the sweep done at 21:19; walk fixes at 20:57. All four steps done; A04 to A10 redrawn at 22:33:48 to 22:34:23, all seven plates fresh.

**The guide check inside page frames, for the main session (22:38 UTC).** The main session's 22:07 call: the quick check of the 21:20:35 build failed 21 times inside chapter 20's frames.
1. `work/build/scripts/phase-2/guide_check.js`: inside a well-formed frame (its page inert and `aria-hidden="true"` in the frame's `role="img"` SVG) the page is a picture, as an image stage's is. `brokenLinks`, `overflow`, `fitSwitch`, the glyph, control and title tests (`iconTargets`, `iconSizes` with D2-517's family, `iconNames`, A-3, A-4, A-8, G-4, C-5), `stateWords` and `forcedGlyphs` leave it alone. The frame keeps its own tests: `pageFrame` (a named SVG, an alt of 15 characters or more, the page inert and hidden), and its words read **at the frame's own width**, the frame's scale divided out, for `under13`, `contrast` (the 8 px floor for a shape behind a word scaled the same way) and `typeScale` (D2-254's sizes for the frame's width, its tokens and the chart sizes as they compute inside it). The 2.6 and 6.5 px sizes in the failures were a tracker's 15 px numbers and a chart's words drawn small by the frame's scale.
2. Six new plants: a frame's 15 and 17 px words, HTML and SVG, drawn under 13 px on screen (allowed); a link to no id inside a frame's page (allowed); 12 px words in a 300 px frame drawn larger than 13 px on screen, caught only by the reading at the frame's own width; the same 12 px words in the stage outside the frame (caught); a frame hidden but not inert (caught by `pageFrame`); a frame with an empty alt (caught by `pageFrame`). Self-test, `--results` in scratch: **PASS, 163 of 163 planted faults caught, 55 of 55 allowed cases left alone** (22:18 to 22:33).
3. **Real at the frame's own width, fixed in the kit** (a probe read every frame at its own width at 1440 and 390 px before and after):
   - The home page at 1440 drew its chart (S10) for its 866.7 px column, but the chart kit caps a reading chart's figure at its 720 px artboard, so the drawing shrank and its 15 and 13 px words showed at 12.46 and 10.8 px (53 words in each 1440 frame and export). `renderers/web-page.mjs` `chart_figure` now draws at most at the chart's artboard. After: 0 words under 13 px and 0 off D2-254 at the frames' own widths.
   - The home page's 390 px first-screen frames (the opener's dark one and both in Rule 20.5's plate) lost the card tracker's hidden step words to the pruning of what starts below the window: 3 of 6 steps had no state in words (A-5). `oa-app.mjs` now keeps a visually hidden word list while its holder starts inside the window. After: every tracker in every frame says each step's state in words.
4. **Not real, left to the skip:** the 51 links to `#a04-...-main` (A04's frames draw the masthead alone, and no reader reaches an inert link); the glyphs at screen sizes (at their own widths every glyph is at its family's size and every 24 px glyph of the 41 carries the 1x and 2x switch); the controls under 44 px (at their own widths only A07's "Individual State Descriptions" link remains, set inline in a paragraph's running text, WCAG 2.5.8's inline exception); contrast (0 pairs under the bar at the frames' own widths; the 390 px "ratio 1" was a mark too small on screen to count as the ground behind its number); forced colors and the missing `data-icon-family` (pictures, as in an image stage).
5. **Outside the frames:** `typeScale`'s `s-20-10-failure` (15.95 and 54.82 px at 1440) is the design director's failure plate in the generator, which holds no kit frame; its card scales with its column. Other failure plates carry `check_exempt: "scale"`; that change is the generator's owner's.
6. Rebuilt in order, each under the lock: generator (22:33:48), kit A04 to A10 (to 22:34:23), generator, strict build (to 22:34:39): **exit 0, 0 warnings, 0 stale plates, 13,080,539 bytes, 393 rules, 731 specimens; chapter 20 839,094 against 757,000 (111 percent); 181,900 under 16 MB.** `check-dimensions.py` 41 of 41; pixel checks 27 of 27 views; C5 90 of 90 screens; the kit's web checks 0 faults on 18 views (axe, each Tab stop's ring); the sweep 0 and 0; frames against exports 18 of 18 identical.
7. **For the accessibility lead:** the working pages changed at 22:33:48 to 22:34:23 UTC (the home page's chart at 1440 px drawn at 720 px; the pages' words and controls are unchanged).

**Craft fixes and sweep, for the main session (21:19 UTC).** The main session's three faults (21:14) and a scripted sweep. Rebuilt in the editor's order, each under the lock: the chapter 20 generator (21:17:41), the kit, A04 to A10 (to 21:18:20), the generator again, the strict build (to 21:18:31).
1. The article's "39,555" ran 44 px past its count panel at 1,024 px (the figure size, 82 px, in a panel 235 px inside). From 64em to 90em, where the grid gives the panel four of twelve columns, the count panel's and the fact box's figures step down the type scale to the section size; 0 px past at every view.
2. "How the Census Bureau counts them" sat 153 px over its paragraph at 1,024 (110 at 1,440): the fact box beside it spanned two grid rows and grew the first. Each section's heading now opens the same body block as its first paragraphs, with the fact box beside that one block: 16 px at every width.
3. "Who decides" sat 4 px under the last line of "What the record shows". A section's h3 after a block now takes 48 px above and 16 below (Rule 07.4).
4. **Found by me while fixing 1:** my DD-5 change had made the status and comment panels query containers, and a container also sets what `cqi` means inside it, so the comment panel's deadline (`oa.type.h4`) drew at 21.6 px where the page's h4 is 24 (1,440) and 21.3 for 22.4 (1,024). The ask's container now wraps the ask alone (its type is a fixed 19 px); the panel's h4 now matches the page's at 1,440, 1,024 and 390 px. The ask still runs 323 by 48 px on one line where its panel has room and 205 by 70 on two lines elsewhere.
5. **The sweep** (`scratch/c11/engineer/tools/sweep.mjs`), on the capture page of each page at all six views: (a) every text run's line boxes against the content box of its nearest ancestor that paints a ground, draws a border or clips, and against the window (a chart table's scroll frame left out, as its scroll is meant); (b) every heading in main and the footer: the gap to the nearest block above against the gap to its own text, flagged when it is no closer to its text, or when it stands more than 40 px over its text outside a panel. Before the fixes: 1 overflow and 7 headings ("Who decides" at six views, the Count heading at 1,440 and 1,024; the relative test alone had missed the Count heading because 339 px of space stood above it). After: **0 text boxes past their containers, 0 headings out of rhythm, at 18 views.** Checked and kept by the spec: the home page's pillar cells and the atlas title bar, panel headings whose 44 to 67 px to the text below includes the panel's padding, each still closer to its text than to the block above.
6. Closing checks on these outputs: strict build exit 0, 0 warnings, **0 stale plates, 13,080,193 bytes, 393 rules, 731 specimens; chapter 20 838,748 against 757,000 (111 percent); 182,246 under 16 MB**. `check-dimensions.py` 41 of 41; pixel checks 27 of 27 views; C5 90 of 90 screens within Rule 05.1 under DR-310; web checks 0 faults on 18 views; W1 rerun 6 of 6 clean; frames against exports 18 of 18 identical.
7. **For the accessibility lead:** the working pages changed again at 21:17:42 to 21:18:20 UTC.

**Walk fixes, for the main session and the accessibility lead (20:58 UTC).** The accessibility lead's W1, W2, W3, W5 and W6 (its notes, "Walks, chapter 20"), fixed in the kit; final kit build 20:56:53 to 20:57:30 UTC, after the generator's last change (20:42:09). **The three working pages changed at 20:49, 20:52, 20:53, 20:55 and finally 20:56:53 to 20:57:30 UTC**; a walk of an earlier copy saw the earlier pages.
- W1 (2.4.11): the site's menu (`.ws .oa-masthead-dialog`, the website's own style, not chapter 18's file) takes `scroll-padding-top: calc(var(--oa-space-800) + 1px)`, and the site's script sets it on opening to the title row's height plus 9 px (the 2 px ring set 2 px out, and air), should the row wrap. The lead's case rerun on the final pages: at 320 by 256 and 390 by 422, Shift+Tab round the open menu on all three pages, 11 or 12 controls each, **0 hidden, 0 partly hidden, 0 rings under the row** (6 of 6 runs). Chapter 18's own fix stays the lead's AL11-2 for Dustin.
- W2: every dark-page rule in the site style (the panels' and cells' 1 px edge, the strip's top edge, L3's links) is also keyed on the device, as `tokens.css` keys the dark tokens (`@media (prefers-color-scheme: dark)` with `:root:not([data-oa-theme="light"])`). Device dark, nothing chosen, 390 px: 6 of 6 Charcoal elements edged on the home page, 4 of 4 on the article and the Act page.
- W3: on the working pages each chart table frame (`.oac-tw`, a group named "…, table") takes `tabindex="0"` (D4-92's pattern); the guide's frames, pictures, take none. Checked on all three pages.
- W5: the home cards' headline links reach 44 px from their own line height (`padding-block: max(0px, (44px - 1lh) / 2)` with the same negative margin): 44 px on one line, 72 on two, at 360 and 390 px; the home captures at 360, 390 and 1440 px are pixel-identical to the 20:42 ones.
- W6 and ED11-4: frame names take the editor's words for A04 to A08 and A10, a period before "At", "in the dark theme", typographer's apostrophes; A09's frame takes the generator's alt (`--page-words A09`), no longer empty. A scan of all 45 frame names finds none empty, none with a straight apostrophe, none running "…part At", none saying "dark mode".
- Closing checks on the final build: `check-dimensions.py` 41 of 41; pixel checks 27 of 27 views; **C5 90 of 90 screens within Rule 05.1** (the article's Step at 1440: 80.4 percent Newsprint); web checks 0 faults on 18 views; frames against exports 18 of 18 identical; strict build 20:57 exit 0, 0 warnings, **0 stale plates**, 13,079,965 bytes, chapter 20 838,520 against 757,000 (111 percent), 182,474 under 16 MB.
- **Run order (the editor's request):** the chapter 20 generator must run after this kit build and before the closing strict build, since Rule 20.9's plate and the files extra read the kit's plates and manifest; the generator's outputs are the design director's, so I did not run it.

**DD-6 round, for the main session (20:26 UTC):**
1. 12.1: from 64em the article's step box spans cols 1 to 12 with its words held to the body's columns by padding (one column and gutter at 1024, two at 1440). The Step screen now measures **81.8 percent Newsprint at 1,440 px** and 79.3 at 1,024 (71.5 at 390, 66.0 at 360): inside Rule 05.1 under DR-310. (The 20:23 drawing measured 88.4 because the body's measure cap still held the box at 542 px; fixed at 20:24.)
2. 12.2: the home page's Track and Act cards draw their six steps, and the Act page's status panel its upright steps, from **chapter 11's own code**: a new kit tool, `work/build/app-kit/tools/ch11_marks.py`, runs `apply_systems_ch11.py`'s `steps_svg` (Rule 11.5's card row: 24 px, the first circle on the text edge, 60 px apart, 57 on the 309 px card at 1440) and `sample` (Rule 11.6's 28 px marks), with its `MARK_CSS` and its state words, read-only. H.R. 7008's step 2 draws the Not yet ring under the 2 px slash with its halo; the NAC rule's step 3 carries the take-part disc. Screen readers get each card's steps in words (Rule 11.2's hidden list, "Step 2, Hearing: never happened."). The ask now shares Rule 11.4's red job, "take part now", with the take-part mark. "What the record shows" prints from the generator.
3. Checks on the redrawn views: `check-dimensions.py` 41 of 41; pixel checks **27 of 27 views pass** (every screen of every page, light and dark, inside Rule 05.1; one red job a view); axe 0, Tab order, theme after reload, reflow 320 px and 200 percent text: 0 faults on 18 views; frames against exports 18 of 18 identical.
4. Strict build 20:26: exit 0, 0 warnings, 13,076,424 bytes, 393 rules, 731 specimens; **chapter 20 835,047 against 757,000 (110 percent)**, reported (DR-271); projection 15.81 MB, 186,015 under 16 MB.
5. **For the accessibility lead:** the three working pages in `work/build/exports/phase-4/` changed at 20:23:05 to 20:23:41 and again at 20:24:56 to 20:25:31 UTC (the trackers, the step box, the ask's red job, the record's two sides); a walk before 20:25:31 saw the earlier pages.

**Summary for the main session (20:16 UTC):**
1. C4 live: specimens ask for the kit's drawing by `<div data-oa-app="A06" data-oa-app-views="...">`; the build places the kit's frames (pictures: SVG named by alt, page inert and hidden), checks each plate's inputs and its own words by hash, puts the kit's styles in the head and its identity masters in one hidden sprite, once each, and weighs them in chapter 20. Headings and landmarks are allowed only inside such frames; guide check `pageFrame` added. Build self-test 40 of 40 (414 expectations); guide check self-test PASS, 159 of 159 faults caught, 53 of 53 allowed cases quiet.
2. C5 live: `tools/screen_shares.py`, per frame and screen, in `export_checks.py` and in each page plate's JSON (R6).
3. C6 live: `share-image` (A09) and `favicon-set` (A10); `check-dimensions.py` learns ICO, SVG and HTML.
4. C7: the website, A04 to A10, from the specs, DD-4 and DD-5, words from the chapter generator; 41 of 41 exports pass the dimension check; 26 of 27 views pass the pixel checks (one screen open, Requests); axe 0, Tab order, theme kept, reflow all pass; 18 of 18 page frames pixel-identical to their exports.
5. Strict build 20:13: exit 0, 0 warnings, 13,014,713 bytes, 393 rules, 731 specimens; **chapter 20 773,336 against 757,000 (102 percent)**, reported (DR-271); projection 15.75 MB, 247,726 under 16 MB.
6. After any word edit in `phase4_ch20_build.py`, rerun the kit (`oa-app.mjs build A04 A05 A06 A07 A08 A09 A10`, under the lock) or the strict build warns a plate is stale.

## Contracts

Chat 10's C1 (photographs), C2 (chapter 16 in the build) and C3 (the application kit) stand in `20261121_Chat-10-Engineer-Notes.md`. Each contract below says when it goes live.

### C4. Page plates in the guide: the kit's frames, their headings and their icons (register row "The article plate's headings and icon path")

Written 19:05 UTC, before the build. **Live since 19:09 UTC** in `guide_build.py` (hook in `work/build/app-kit/tools/app_plates.py`) and `guide_check.js` (19:27 UTC). Revised 19:52 to 20:00: freshness of words by hash (below), the overlay switch, the title line.

**How a chapter asks for an application.** A specimen file holds one placeholder where the kit's drawing goes, as a chart specimen holds `data-oa-chart`:

```html
<div data-oa-app="A05" data-oa-app-views="1440-light 390-light 390-dark"></div>
```

- `data-oa-app`: the application's id (`A04` on; the content file `work/build/app-kit/specs/a05-*.json`).
- `data-oa-app-views` (optional): which of its frames, in that order, by view key: `<width>-<theme>` (`1440-light`, `390-dark`), or `<width>-<theme>-<state>` where the spec draws states (`390-light-open`, the menu open). Left out, every frame the kit drew, in the spec's order. An unknown key is a build warning.
- `data-oa-app-title` (optional, web pages): prints the page's own `<title>`, read from the kit's plate, on a line above the frames, led by the attribute's words, for example `data-oa-app-title="Page title"` (AL-01: "copied from the page's markup by the renderer, never typed twice").
- Nothing else inside the placeholder. The specimen keeps its own words around it (a label line, a key) as any specimen does. Never copy a frame's markup into a specimen: markup carrying `data-oa-page-frame` in a specimen's own file is a build warning, so `--strict` fails.

**Where the drawing comes from.** A content file that sets `"guide": true` gets a guide plate: `node work/build/app-kit/oa-app.mjs build A05` (under the lock) draws the application and writes `work/build/app-kit/plates/a05.json`: its frames (view key, width, height, alt, markup, and for a page's full-length views its `screens`, R6), `inputs` (every file the kit read or imported to draw it, with its SHA-256) and `words` (the hash of that application's entry in the chapter generator's `--page-words all` output). The guide build puts the frames in place of the placeholder and checks both: a changed input or changed words is a warning ("run oa-app.mjs build A05"), so a strict build never prints a stale drawing. Words are checked by their own hash, not the generator file's, so an edit to one page's words stales only that plate. **After any word edit in `phase4_ch20_build.py`, run `node work/build/app-kit/oa-app.mjs build A04 A05 A06 A07 A08 A09 A10` under the lock** (about 3 minutes); it also rewrites the exports. The kit's shared style for each renderer type (`plates/<type>.css`) goes into the page once, in the head (`<style data-oa-app-kit="web-page">`), and weighs against the chapter whose section first draws that type (chapter 20 for `web-page`).

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

**What a frame carries.** Only what its width can show: the kit renders each frame alone at its width, removes what the page sets `display: none` there (the other wordmark masters, Menu or the bar's switch, the closed dialog, a closed disclosure's contents) and, for a one-window view, everything that starts below the window, and keeps the result only if a capture before and after is the same pixel for pixel (every frame passed). A frame keeps only the chart drawing its column shows (R4), drawn at that column's width (R8).

**Identity masters once for the page** (added 20:07 UTC, step 4). In a guide frame each identity master (L3, the lockmark, ampersand B's masters, chapter 18's two wordmarks) is an `<svg>` around a `<use>` of one `<symbol>`; the plate JSON carries the symbols (`symbols`), and the build puts each once in a hidden `<svg data-oa-app-kit="identity">` at the top of the body (13,105 bytes for seven masters), counted in chapter 20. The kit captures every frame before and after the swap and stops if one pixel differs (it caught L3's viewBox, which starts at y −12, on its first run). Exports keep their masters inline.

**An overlay.** A plate whose frame carries a safe-area layer (A10's 512 px icon) gets C3's switch, a native checkbox labeled by the plate JSON's `switch_words` ("Show the safe areas" until the editor words it).

### C5. Color by screen, for DR-310 (Rule 05.1 on a long page)

Written 19:05 UTC. **Live since 19:43 UTC**; revised 19:47 and 19:51 (below, marked).

**What it measures.** On a page capture, Newsprint, dark (Charcoal plus Prussian) and Pillar Red shares, and the dark panels, for the page's first screen and for each section's opening screen; Rule 05.1 as DR-310 words it. A screen is the window's height at that width (the spec's `vh`: 900 at 1440, 768 at 1024, 844 at 390, 780 at 360 unless the page spec sets others).

**How a page marks its sections.** Put `data-oa-section="<short name>"` on the outer element of each section after the first screen (for example `<section data-oa-section="Track" ...>`). Its top edge starts that section's opening screen: from its top down one window's height; **for a section that starts within a window of the page's end, the page's last window** (revised 19:47: a reader can scroll no further, so the footer's own screen is the last window). The first screen (0 to one window) is always measured and needs no mark. A dark panel is any element painted Charcoal or Prussian (read from the computed background, the outermost of nested ones) of **1 percent of a screen or more** (revised 19:51 from 3: a 1,440 px home page cell is 2.7 percent; a button stays under 1), and it **counts in the section whose element holds it** (revised 19:47: side-by-side sections at 1,024 px each keep their own cell); one in no section counts with the first screen. The footer carries `data-oa-section="Footer"` and is its own section (R2).

**What it judges.** A light frame: Newsprint 60 to 85 percent, at most one dark panel per section, Pillar Red (signature red included) within 5 percent, on each measured screen. A dark frame: its shares and panels are printed, and only the red limit is judged (Rule 05.1's Newsprint share is the light view's; the dark mode is DR-204's). Pixels count as a color within 3 levels on each channel of the token (24 for red, which antialiasing spreads).

**Working red on a long page** (added 19:46): two working reds of different jobs (`data-red-job`) may not stand within one window of each other; marks of one job, the take-part mark and its ask (Rule 11.4), may share a view.

**How to run it.** The kit records each frame's sections and panels when it captures the frame, writes each full-length view's screens into the page plate's JSON (`views[].screens`: `name`, `newsprint`, `dark`, `red`, `panels`, `panels_box` in percent of the screen, R6), and `python3 -I work/build/app-kit/tools/export_checks.py OUT EXPORTS` prints a line per frame and screen, for example `1440 light, first screen: Newsprint 71.2, dark 14.0, red 0.3; 1 panel` with PASS or FAIL. Alone, on any capture: `python3 -I work/build/app-kit/tools/screen_shares.py CAPTURE.png --vh 900 --sections "Track:1320,Act:2980" [--theme light] [--json OUT]`, or `--batch IN.json OUT.json`.

### C6. The share preview and the favicon set as kit types

Written 19:05 UTC. **Live since 19:36 UTC.** A09 follows the page specs' section 8 (a Charcoal foot band holding the wordmark and the sign-off); A10 takes its ink from the generator (`favicon_ink`). Files: `20261121_Web-Share-Preview-Special-Districts-1200x630.png`, `20261121_Web-Favicon.svg` (serve as `favicon.svg`), `20261121_Web-Favicon-16-32-48.ico` (`favicon.ico`), `20261121_Web-Apple-Touch-Icon-180.png` (`apple-touch-icon.png`), `20261121_Web-Manifest-Icon-192.png`, `20261121_Web-Manifest-Icon-512-Maskable.png`; each entry in the manifest names its `serve_as`.

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


### C7. The website kit (for the design director, the accessibility lead and the editor)

Written 20:04 UTC; live since 19:49 UTC.

- **Renderer** `work/build/app-kit/renderers/web-site.mjs` (type `web-site`), with `renderers/site-parts.mjs` (chapter 18's masthead, dialog, switch and scripts, read from their files; the website's close-on-widen script, AL-06). Content files `specs/a04-web-masthead-and-menu.json` to `a10-web-favicons.json` hold layout keys only; **every word comes from `phase4_ch20_build.py --page-words all`**, read-only, as DD-3 sets, in the shape the generator prints (each application's own entry with its `site` words; A04 and A05 take `article`).
- **Views** (C4 keys): A04 `1440-light` to `390-dark` (the masthead band) and `390-light-open`, `360-light-open`, `390-dark-open` (one window, the menu open); A05 the footer band at five views; A06 the six full-length views and `1440-light-screen`, `390-light-screen`, `390-dark-screen` (R1); A07 and A08 the six full-length views; A09 `1200-light`; A10 `tab-light`, `tab-dark`, `ico`, `180`, `192`, `512` (the 512 with its safe circle as an overlay).
- **Working pages, for the accessibility lead's walks** (AL request 1): `work/build/exports/phase-4/20261121_Web-Home-Page.html`, `20261121_Web-Article-Page-Special-Districts.html`, `20261121_Web-Act-Page-Comment-On-A-Proposed-Rule.html`. Each is one self-contained file (fonts, tokens, sprite, chapter 18's scripts and the head script); `<html lang="en">`, the page's `<title>` per AL-01, the theme follows the device until chosen, and the choice is kept under `oa-theme`. Menu opens chapter 18's modal dialog with focus on the current part (or Close the menu on the home page); Escape returns focus to Menu with `aria-expanded="false"`; widening past 64em with the menu open closes it and puts focus on the current part's link in the bar or the home link (AL-06, request 2). The skip link is the first stop and moves focus to `main`. Captures of every width and theme sit beside each page, and `20261121_Web-Menu-Open-390-Light.png`, `-360-Light.png`, `-390-Dark.png` show the menu open.
- **Title line** (AL request 3): a specimen adds `data-oa-app-title="Page title"` to its placeholder and the hook prints the page's own `<title>` above the frames (C4).
- **The page in each theme.** Light and dark frames set `data-oa-theme` on the frame's root; the switch in each frame shows that theme checked. On the dark page every Charcoal panel and the head cells draw a 1 px `--oa-color-border-hairline-on-charcoal` edge (Rule 20.5's correct plate).
- **Charts** S10, S66 and S86 are the chart kit's own figures (its `run_spec`, `K.draw`, `K.figure`); a frame or capture carries the one drawing its column shows, drawn at that column's width (R4, R8); the working page keeps the kit's lean pair (desk 541 or 621 px, phone 328 px).
- **Manifest** entries carry `spec` and `size` words a plate can print (R7), for example "1,440 by 2,950 px", "16, 32 and 48 px", "the working page, at any width".

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
- D4-xxx | The website is one renderer type, `web-site`, for every page and part (A04 to A08), with chapter 18's masthead, dialog, switch and scripts read from their files and changed only by DR-307's parts, the site's breakpoints and the switch's two places | One source draws the masthead and footer for every page, so 3.2.6's help link cannot drift (AL-04); chapter 18 stays approved and unchanged
- D4-xxx | The working pages are exports in their own right (HTML), and every PNG of a page is captured from them | The accessibility lead's walks need working pages; DR-298's site is HTML and CSS from the tokens; the captures then show the page a reader gets
- D4-xxx | The parts sit in the bar from 64em and the switch on a row under it; under 64em Menu opens the dialog with the switch at its top; the bar's breakpoints are container queries on the page's root, which resets to 1rem | The page specs' section 2; a container query's em reads the container's own font size, so `.ws` takes `1rem` and the body type moves to its inner block (found at 19:40: 90em had become 1,530 px)
- D4-xxx | On the Act page, while a step of the status panel is pending (Request R3), the steps print as words with no circles and the pending step is left out; the take-part mark goes with the circles, and the ask carries the view's working red | DD-3: "while `pending` is not empty the kit draws the status words and no circles"; I read the status panel's `pending` as the tracker's
- D4-xxx | A docket number in the ask stays on one line (`white-space: nowrap` on the text, never the address) | It is an ID; the 19:44 drawing broke "FDA-2025-N-" from "2699"
- D4-xxx | Each frame and each capture draws its chart at the column it fills (R8); the working page keeps the kit's lean pair at its narrowest columns | No frame scales a drawing past its true size; the working page must serve every width from one file
- D4-xxx | Kit frames carry only what they show, proved by a capture before and after pruning, pixel for pixel | 30 to 88 percent of each frame's markup was invisible there (closed disclosures, other widths' wordmarks, the closed dialog, below the window)
- D4-xxx | The A10 plate draws the favicon in `currentColor` set from `--oa-color-identity-signature-on-white` and `-on-charcoal`; the exported SVG keeps the literal color the token resolves to | R9: a guide frame takes no literal color; a favicon file reads no stylesheet
- D4-xxx | In guide frames, each identity master is drawn by `<use>` of one symbol the page carries once, proved pixel for pixel per frame; exports keep them inline | 161 KB of the same seven drawings repeated across 43 frames; the C1 pattern (one copy for the page); chapter 20 fell from 885,184 to 773,336 bytes
- D4-xxx | A plate's freshness covers its own words by hash of its entry in `--page-words all` (A10 also the home page's, for its tab title), not the generator file | Every word edit anywhere staled all seven plates; now only the plate whose words changed
- D4-xxx | The ask breaks into its two phrases and stays as wide as the longer one wherever its panel has less room than its words (a container query at 19rem on the panel), one line elsewhere | DD-5 11.4 ("as wide as its words, never stretched"); the 1,024 px status panel has 235 px inside, so the window's width could not decide it; rem, since the status box sets 15 px type
- D4-xxx | The article's closing step (the paragraph that ends on B) stands in the step box; the fact box's source line stands under the box | DD-5 11.1 and 11.2
- D4-xxx | The trackers' marks are drawn by chapter 11's own generator code through `tools/ch11_marks.py` (`steps_svg`, `sample`, `MARK_CSS`, `STATE_WORD`), read-only; the marks' color variables are set on the element that holds them | The main session's 20:23 instruction ("reuse chapter 11's drawing of the marks from its source, never a copy"); chapter 18's tracker draws 26 px marks, and the cards take Rule 11.5's 24 px; variables set on the holder resolve inside a Charcoal panel
- D4-xxx | The ask's red job is "take part now", Rule 11.4's own, shared with the take-part mark | Rule 11.4's builders; the page's window rule allows two reds of one job in a view
- D4-xxx | From 64em the step box drops the body's measure cap (its words keep it) | 12.1; the cap had held the box at 542 px
- D4-xxx | W1's scroll padding lives in the website's own style and script, scoped to the site's menu; chapter 18's file is unchanged | Chapter 18 is approved; the main session's 20:47 instruction; the lead's tested value with room for the ring
- D4-xxx | The headline links' 44 px targets come from their own line height (`1lh`), with negative margins, so no type moves | AL-15; a fixed 6.5 px gave 41 px on a phone, whose h3 line is 28 px
- D4-xxx | A panel's figure steps down to the section size from 64em to 90em, keyed on the page's container, where the grid makes the panel four of twelve columns | A figure must fit its panel (the main session, 21:14); the panel cannot be a query container itself without changing what its fluid type's `cqi` means
- D4-xxx | The ask's query container is a wrapper around the ask alone, not its panel | Making the panels containers set the comment panel's h4 by the panel's width (21.6 px for the page's 24 at 1,440), a fault of mine from DD-5, found 21:15
- D4-xxx | A section's heading opens the body block of its first paragraphs; a panel beside them sits in that one grid row | Rule 07.4: the text stays directly under its heading whatever stands beside it
- D4-xxx | A section's h3 after a block takes 48 px above and 16 below | Rule 07.4 and the specs' section rhythm; "Who decides" sat 4 px under the block above
- D4-xxx | The craft sweep reads Rule 07.4 as the main session words it (closer to its own text than to the block above) plus a 40 px ceiling on the gap to its own text outside a panel | The relative test alone passed a heading 153 px over its text when the space above it was larger still
- D4-xxx | I ran the chapter 20 generator (twice, under the lock) in the rebuild order | The main session's 21:14 instruction; the generator's outputs are the design director's and the editor's words, which I did not touch
- D4-xxx | The exports manifest is one file for the folder: a build of some applications replaces their entries and keeps the others' | Chat 10's command rewrote the manifest with only the applications it built, which would drop A01 to A03 from `check-dimensions.py` on the next build
- D4-xxx | Inside a well-formed page frame the guide check treats the page as a picture, as it treats an image stage: live-content tests skip it; `pageFrame`, `under13`, `contrast` and `typeScale` read it at the frame's own width | The main session's 22:07 call; a frame scaled into a column drew a page's 15 px words at 2.6 to 6.5 px, which no reader of the page meets
- D4-xxx | A chart in a website page draws at most at its artboard's width | The chart kit's style caps a reading chart's figure at 720 px; drawn for the home page's 866.7 px column, it shrank and set 15 px words at 12.46 px
- D4-xxx | A one-window view's pruning keeps a visually hidden word list whose holder starts in the window | A tracker the window shows keeps its steps' states in words (A-5); the list draws nothing, and the pruning's before and after captures still match

## Done

Step 1, the three "now" items (19:05 to 19:43 UTC).

| Item | What changed | Files | Proof |
|---|---|---|---|
| (a) Page plates: headings, icons, a narrow allowance (C4) | The kit writes guide plates with frames whose page is inert and hidden; the build places them from a placeholder, checks freshness, keeps the kit's style once in the head and weighs it in chapter 20; headings, landmarks and controls allowed only inside such frames; every icon by `<use>` of the guide's sprite (chapter 18's check, menu and close icons converted as read) | `work/build/app-kit/lib.mjs` (frame `page`, `track`, `touch`, `sha256`, `token_value`, circle overlay), `oa-app.mjs`, `tools/app_plates.py` (new), `renderers/web-page.mjs` (`sprite_icons`, chart widths); `work/build/scripts/phase-2/guide_build.py` (import, `process_fragment`, `plate()`, page head, `weigh()`, `--app-plates`, a self-test scenario); `work/build/scripts/phase-2/guide_check.js` (`inPageFrame`, `pageFrame`, `typeScale` probe, nine plants) | `app_plates.py --self-test` 12 of 12; `guide_build.py --self-test` 40 of 40 scenarios, 414 of 414 expectations (was 39 and 395); `guide_check.js --self-test --results <scratch>` PASS: clean demo passes, 159 of 159 planted faults caught, 53 of 53 allowed cases left alone (19:27); strict build identical to the baseline but its built time (19:09) |
| (b) Color by screen (C5) | `tools/screen_shares.py` (new) and its use in `tools/export_checks.py`; the kit gathers sections, dark elements with their section, and each red with its job | `work/build/app-kit/tools/screen_shares.py`, `tools/export_checks.py`, `oa-app.mjs` | `screen_shares.py --self-test` 9 of 9 |
| (c) Share preview and favicon set (C6) | Two renderer types, an ICO writer, ICO, SVG and HTML in the dimension check, the icon checks | `renderers/share-image.mjs`, `renderers/favicon-set.mjs` (new), `tools/ico.py` (new), `check-dimensions.py`, `tools/export_checks.py` | `ico.py --self-test` 2 of 2; `check-dimensions.py --self-test` 13 of 13 cases right |

Step 2, the website (19:28 to 20:00 UTC): `renderers/web-site.mjs` and `renderers/site-parts.mjs` (new); content files `specs/a04` to `a10` (new); DD-4's five revisions (19:56). Plates in `work/build/app-kit/plates/` (`a04.json` to `a10.json`, `web-site.css`, `share-image.css`, `favicon-set.css`).

Step 3, exports (20:00 UTC): 30 new files in `work/build/exports/phase-4/` (three working pages; 18 page captures; three menu captures; the share preview; six icon files) beside chat 10's 11; `20261121_Phase-4-Exports-Manifest.json` holds all 41. `check-dimensions.py`: **41 of 41 pass.**

**Contrast, measured on the exports' pixels** (`tools/export_checks.py`, word by word; lowest pair per page):

| Pair | Where | Ratio |
|---|---|---|
| Charcoal on Newsprint | every light page's text | 13.29 |
| Deep Stone on Newsprint | secondary words, captions, source lines | 5.49 (the lowest on every light page and the share card) |
| Dim Newsprint on Charcoal | panels' secondary words, every dark page's secondary words | 7.26 (the lowest on every dark page but the Act page's) |
| White on Pillar Red | the Act page's ask, 19 px bold (large text, 3 to 1 needed) | 4.17 |
| Pillar Red on Charcoal | the app icons' B (a mark, 3 to 1 needed) | 4.49 |

**Rule 08.2's feed test, dark card** (A09): 500 px wide, 8 of 8 nodes, 45 red pixels; 360 px, 8 of 8 nodes, 24 red pixels. Newsprint 60.8 percent of the card (the band 31.7).

**Icons** (A10): the ICO holds 16, 32 and 48 px PNGs; B stands 104, 112 and 296 px in the 180, 192 and 512 px tiles (57.8 to 58.3 percent); on the 512 its ink reaches 197.4 px from the center, inside the 204.8 px safe circle.

**Screens (C5) after DD-5** (20:13 UTC): every screen passes but the article's Step at 1440 px (90.8 percent Newsprint); 26 of 27 views pass all their pixel checks. Before DD-5, after DD-4 (20:00 UTC): 52 of 60 light screens passed. Fail: article Step 87.8 (1440), 95.3 (1024), 90.3 (390), 88.8 (360) percent Newsprint; article Count 56.0 (390) and 49.8 (360); Act Proposal 88.6 (1440); Act Comment red 6.27 percent at 390. Every first screen passes (home 81.7, 77.5, 71.6, 70.6; article 81.0, 80.3, 69.3, 76.8; Act 72.6, 69.5, 69.1, 73.2). On the dark pages 29 of 30 screens pass; the Act page's Comment screen at 390 px fails the same red limit (6.27 percent).

**Web checks on the working pages** (each width and theme): axe 0 violations at all 18 page views; Tab order at 1440: skip link, home, the seven parts, the switch (one stop), then content; at 390: skip link, home, Menu, then content; each stop with a 2 px ring; Dark chosen at 1440, reloaded: the root is dark, `oa-theme` holds dark and both switches show Dark (and Light the same); 320 px: nothing wider than the window; 200 percent text at 1024 px: nothing wider. Menu: opens with focus on Explain (the current part), Escape closes it with focus on Menu and `aria-expanded="false"`, at 390 and 360 light and 390 dark.

**Frames against exports:** every page frame of A06, A07 and A08 rendered at true size beside its export capture: **18 of 18 identical, 0 differing pixels** (the frame 1 px taller in 10, an empty row from rounding up).

Step 4, bytes. At 20:02 UTC (strict build, the design director's chapter 20 in place) chapter 20 weighed 885,184 bytes against 757,000 (117 percent). The identity sprite (20:07) brought it to 761,278; after DD-5 and the sprite counted whole (its first measure stopped at L3's nested `</svg>`), **773,336 bytes against 757,000 (102 percent)** at 20:13, reported, not failed (DR-271); the page 13,014,713 bytes; projection 15.75 MB, 247,726 under 16 MB. Counted in chapter 20 from outside its section: the kit's styles in the head (web-site 44,695 at 20:09, plate 2,296, share-image 1,990, favicon-set 1,050) and the identity sprite (13,105). `guide_charts.py`'s allocation for chapter 20 stays 757,000; nothing in the projection's method moved. Each plate as placed (its figure, frames, caption and words), strict build of 20:13:

| Plate | Bytes | Frames |
|---|---|---|
| s-20-opener (A06) | 24,182 | 2 |
| s-20-1-correct (A04) | 15,625 | 6 |
| s-20-2-correct (A04) | 14,043 | 3 |
| s-20-3-correct (A05) | 14,215 | 5 |
| s-20-5-correct (A06) | 10,710 | 2 |
| s-20-6-correct (A06) | 180,282 | 6 |
| s-20-7-correct (A07) | 101,175 | 6 |
| s-20-8-correct (A08) | 160,634 | 6 |
| s-20-10-correct (A09) | 7,713 | 1 |
| s-20-11-correct (A10) | 11,874 | 6 |
| All plates with kit frames | 540,453 | 43 |

The chapter's section holds 708,626 bytes; the rest of its 773,336 is the kit's styles and sprite (64,710 at 20:13). What weighs most in a page frame is the chart kit's figure (S10, S66, S86 at the frame's column), which is content.

DD-6 round (20:22 to 20:26 UTC): `renderers/web-site.mjs` (trackers, upright marks, step box, ask job), `tools/ch11_marks.py` (new); plates `a04.json` to `a10.json` and the 30 website exports rewritten at 20:24:56 to 20:25:31. Each plate as placed after this round is in the strict build of 20:26; chapter 20 835,047 bytes.

## Requests

- **Design director:** after DD-6 (20:25 UTC) every screen of every page passes Rule 05.1 under DR-310, the article's Step at 1440 included (81.8). The numbers per frame are in `plates/a06.json` to `a08.json`, `views[].screens`.
- **Design director:** R1, R2, R4, R6, R7, R8 and R9 are done (C7). The A10 plate's overlay switch reads "Show the safe areas" (C3's words) until the editor words it: a key for it in the generator (A10 `switch_words`) would let me read it from there.
- **Design director:** the Act page's status panel prints steps 2 to 6 as words, no circles, while step 1 is pending (my reading of DD-3; Routine calls). If you want circles for 2 to 6 with step 1 left out, say so and it is one switch.
- **Accessibility lead:** your three requests are met (C7): the working pages' paths, AL-06's close-on-widen, the title line by `data-oa-app-title`.
- **Main session:** after any change to the chapter generator's words, the kit must be rerun (`node work/build/app-kit/oa-app.mjs build A04 A05 A06 A07 A08 A09 A10` under the lock) or the strict build warns that a plate is stale; a plate goes stale only when its own words change.
- **Main session:** the guide check's self-test ran under the lock for 15 minutes (19:13 to 19:28), holding other owners' builds; it builds only a demo page in a temporary folder, so I suggest it need not take the lock.

### Earlier requests from chat 10, answered here

- Chat 10's "Design director and chapter 20's builder: placed in the guide as a plate, the article frames hold 16 headings ... and chapter 18's switch markup inlines the Selected check path": settled by C4 (register row "The article plate's headings and icon path").

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

- C4: `app_plates.py --self-test` (12); `guide_build.py --self-test` (40 scenarios, 412 expectations) at 19:08, 19:33 and 20:01, and 414 at 20:06 with the identity sprite's case; `guide_check.js --self-test --results` (scratch) at 19:13 to 19:28, PASS (and again at 22:18 to 22:33 after the 22:07 change, PASS); strict builds at 19:04 (baseline), 19:09, 19:33, 20:02, 20:08, 20:09 and 20:13, each exit 0 with 0 warnings (one at 20:06 failed on stale plates, as it should, while the kit stopped on L3's pixel proof; rerun clean); the built guide's masthead, article and favicon plates captured in Chromium and looked at; a fixture chapter 20 (every view of A04 to A10) built strictly at 19:59, exit 0, 0 warnings, after the stale check had caught four plates older than the kit's code and seven older than the generator's words.
- C5: `screen_shares.py --self-test` (9); the measure on every light and dark page capture.
- C6: `ico.py --self-test`; `check-dimensions.py --self-test` (13 cases); `check-dimensions.py` on the exports, 41 of 41; the icon checks; the feed test on A09.
- The pages: axe, Tab order, theme after reload, reflow at 320 px and text at 200 percent, on every view of A06 to A08 in Chromium, last at 20:13 (0 faults); the menu's open and Escape states at 390 and 360 px; frames against exports (18 of 18, pixel for pixel, at 19:45 and again at 20:14 with the identity sprite); pruning proved per frame by captures before and after (all identical); contrast word by word on every export. I looked at the home page at 1440, 1024 and 390 px, the article at 1440 and 390 px light and dark, the Act page at 1440 and 390 px, the menu open in three captures, the share card and the maskable icon.
- The 22:07 call: `guide_check.js --self-test --results` (scratch) PASS, 163 of 163 caught and 55 of 55 allowed (22:33); a probe (scratch `tools/frame-probe.cjs`) on the 21:20:35 build and on my 22:34:39 strict build, every one of the 43 frames at its own width at 1440 and 390 px: before, 106 words under 13 px in the home page's 1440 frames and three 390 px frames short of step words; after, 0 and 0; strict build exit 0, 0 warnings; `check-dimensions.py` 41 of 41; `export_checks.py` 27 of 27 views and 90 of 90 screens; the kit's web checks on 18 views; the sweep; frames against exports 18 of 18.

## Not tested

- The guide check's full run on a page with chapter 20 in place, at any width: the main session runs the closing checks. Its self-test ran (22:18 to 22:33, fixture frames), and my own probe read every frame of the 22:34:39 build at its own width at 1440 and 390 px (words under 13 px, off D2-254, contrast, glyph sizes, targets, step words, links); the quick check itself did not run here.
- The accessibility lead's walks after 22:34:23, and W1's rerun: not repeated for this change.
- Safari and Firefox: only Chromium is installed. The working pages use container queries, `:has()`, `inert`, `<dialog>` and CSS `@scope` in the guide; each is in current Safari and Firefox by their published compatibility data, which I did not open this chat.
- A screen reader on the working pages; the accessibility lead's walks are hers.
- The working pages on a real 2x screen: captures ran at 1x; the 2x drawings (the end mark's master, the icons' masters) were not captured.
- The favicon in a real browser tab and the ICO on Windows; the manifest icons on Android (no `site.webmanifest` is exported).
- Print emulation and forced colors on the pages.
- Chat 10's A02 sample was not redrawn: its renderer now draws the Selected check from the sprite, so its exports would change if it were rebuilt.
