# Chat 10: engineer notes

Status: 02:27 UTC. Started 01:36 UTC. Job 1 done 02:02. Job 2 stopped 02:06 on a refused install, resumed 02:08 on the main session's two answers, done 02:27.

**Job 1 summary (02:03 UTC), for the main session:**
1. P4-5: photographs drawn by name from one copy per page (contract C1), by CSS content replacement on each `<img>`; chapter 01's three plates changed only their `src`.
2. 190,804 bytes freed (12,210,920 to 12,020,116); chapter 01 675,807; new "photographs" part 489,462.
3. Rules 01.6 and 01.8: 36 of 36 captures pixel-identical (1440, 1024, 390, 360 px at 1x; 1440 and 390 at 2x).
4. G3-05: the edge guard holds every word of every chart, and the fan chart's key is on by default; kit 96 of 96, all 192 written files and all 376 drawings hash the same before and after.
5. Projection: Phase 4's seven allocations (3,010,000) in `guide_charts.py`; each built Phase 4 chapter reported against its own; projection 15,460,028, 39,972 under 15.5 MB.
6. Chapter 16 builds in place with no further change (contract C2, proved on a fixture).
7. Closing: strict exit 0, 0 warnings, 12,020,117 bytes; build self-test 39 of 39; chapter 14 check 99 of 99. The guide check's new `photoDrawn` is yours to run.
Job 2 is under way: the sample specs and the specifications JSON are both in.

**Job 2 summary (02:27 UTC):** the application kit (`work/build/app-kit/`, contract C3) drew the three samples; 11 exports in `work/build/exports/phase-4/`, 11 of 11 against the specifications table; pixel checks 8 of 10 (the article's light captures at 1440 and 1024 run 88.2 and 85.9 percent Newsprint, past Rule 05.1, for the design director); axe 0 at all eight web views. Placed plates: post 11,696, article (4 widths, 2 themes) 187,145, report page 11,355. Re-sized Phase 4: 3,284,000 bytes (Gate 3: 3,010,000); projection 15,734,059, 265,941 under 16 MB, now an early-warning note past 15.5 MB. Report PDF fonts: Inter Type 3, Inter Tight CID TrueType (NF-E1).

## Contracts

### C1. Photographs: one copy for the page, drawn by name (P4-5)

Written 01:40 UTC and revised 01:45 UTC, before the build, so chapter 16 can be planned and built against it. **Live since 01:51 UTC** in `guide_build.py`, with `work/build/scripts/phase-4/guide_photos.py`; chapter 01 draws this way now. **The 01:45 version replaces the 01:40 one**: a prototype showed that an SVG `<use>` drawing resamples the photograph differently from `<img>` (softer at 1x, mean 2 to 3 levels off), so chapter 01 would have changed on screen. The request stays an `<img>`, and it draws the one copy through CSS content replacement, which matched today's plates pixel for pixel in Chromium at 1440, 1024, 390 and 360 px, at 1x and 2x. The build side lands in `guide_build.py`; this section says when it is live.

**What changes.** Today a specimen embeds a photograph by its file path, `<img src="work/build/assets/photography/....jpg">`, and the build turns each path into a data URI inside that plate, so a photograph placed twice is carried twice (the Lake Isabella photograph sits in Rule 01.8's correct and failure plates: 190,992 bytes twice). From this chat a specimen asks for a photograph by name. The build carries each named photograph once for the whole page, in one style block in the page's head, `img[data-oa-photo="<name>"]{content:url(data:image/jpeg;base64,...)}`, and every `<img>` that names it shows that one copy. No script is involved. CSS content replacement is standard track and supported since Chrome 28, Firefox 63 and Safari 9 (MDN's compatibility data, read 01:43 UTC).

**The photographs a specimen may name.** Each is the studio's 1,200 px rendition that chapter 01 shows (DR-238), with its rights row and sidecar in `work/build/assets/photography/`.

| Name | Photograph | Pixels | Rights row | File |
|---|---|---|---|---|
| `rotunda-2005` | Members of the public file past the casket of Rosa Parks as she lies in honor in the Capitol Rotunda, October 2005. Architect of the Capitol | 1200 x 797 | pho-01r (rendition of pho-01) | `20261112_Photo-Rule-01-6-Rosa-Parks-Lying-In-Honor-Capitol-Rotunda-2005-1200-Wide.jpg` |
| `lake-isabella-2014` | Paul Zianno of the Corps of Engineers at a public meeting in Lake Isabella, California, March 27, 2014. John Prettyman, U.S. Army | 1200 x 768 | pho-04r (rendition of pho-04) | `20261112_Photo-Rule-01-8-Corps-Of-Engineers-Public-Meeting-Lake-Isabella-2014-Zianno-1200-Wide.jpg` |

A new photograph joins this list only through the engineer (the registry is `PHOTOS` in `work/build/scripts/phase-4/guide_photos.py`), and only with a rights row. Each photograph's caption, credit, date and place are in its sidecar JSON beside the file.

**How a specimen asks for one.** An `<img>` with no `src`, naming the photograph, with its own alt:

```html
<img data-oa-photo="lake-isabella-2014" alt="An official points to a project map while two residents, seen from behind, listen." class="ph r32" width="1200" height="768">
```

- `data-oa-photo`: a name from the table. An unknown name is a build warning, so `--strict` fails.
- `alt`: written for this use, as for any image. Every use carries its own; two plates may show one photograph with two alts and two crops. `alt=""` marks a decorative use. A request with no `alt` is a warning. Inside an image stage (the plate's alt is what a screen reader hears, the picture hidden), the photograph's alt counts as any `<img>` alt does today.
- `width` and `height`: optional size hints, as today; give the photograph's own pixels.
- **The crop, way 1 (CSS, as chapter 01 does).** Style the `<img>` in the plate's CSS: `display:block; width:100%; height:auto; object-fit:cover; aspect-ratio:3/2; object-position:50% 0%`. The frame takes the ratio you set, and `object-position` says which part of the photograph stays (first value across, second down; `0%` is the left or top edge). This shows the largest crop of that ratio.
- **The crop, way 2 (a tight crop).** Add `data-oa-crop="x y width height"`: the rectangle to show, in the photograph's own pixels (the table's sizes), whole numbers, inside the photograph. The build wraps the `<img>` in a frame of that rectangle's ratio (a `<span>` that takes the `<img>`'s `class` and `style`, `overflow:hidden`) and places the photograph so the rectangle fills the frame. Use it for a detail, a face, or a crop that leaves something out. Do not set `object-fit` or `aspect-ratio` for that use; the frame's class may set width, border and margins.
- **Sharpness.** The copy is 1,200 px wide. A crop looks sharp on a 2x screen while its width in photograph pixels is at least twice the width the frame shows in CSS pixels: the whole width suits a frame up to 600 px; a crop 600 px wide suits a frame up to 300 px.
- **Marks over a photograph** (a crop guide, a box around a face, a third line): set them in HTML over the frame, in percent of the frame, inside a wrapper with `position:relative`, colored only by `var(--oa-...)`.
- **Never** embed a photograph file by `src` path, as a CSS `url()` or as a data URI in a specimen. From this chat the build warns on any file under `work/build/assets/photography/` placed by path, so `--strict` fails.
- **A scratch page** that shows a fragment outside the guide needs the photographs' style: `guide_photos.photo_style(["lake-isabella-2014"])` returns the `<style>` block; `guide_photos.photo_img(name, alt, cls="", crop=None)` writes a request tag.

**What the page carries.** The `<img>` as the specimen wrote it (no `src`), and, once per page, in the head, `<style id="oa-photos">` with one rule for each photograph the page names. The specimen file keeps the request; never write the data by hand.

**Bytes.** The photographs weigh as a part of the page of their own, "photographs", outside every chapter: 489,284 bytes of image data for the two, plus about 60 bytes of rule each. A use costs only its `<img>` tag (about 150 bytes, with its alt). So chapter 16's figure counts its tags and none of the photographs, as the Gate 3 report's allocation assumed.

**Chapter 01, the new way.** Rule 01.6: `data-oa-photo="rotunda-2005"`, class `ph r53` (5:3 from the top, `object-position:50% 0%`). Rule 01.8, both plates: `data-oa-photo="lake-isabella-2014"`, class `ph r32` (3:2, centered). Only the `src` changes in their three tags.

### C2. Chapter 16 in the build (for the design director)

Proved at 01:56 UTC with a fixture chapter 16 (two rules, three plates, two photograph requests) built strictly into a copy of today's chapters: the page puts `16-photography.json` in place of the placeholder, under Evidence and media (`<section class="chapter chapter--grouped" id="photography" data-part="evidence" data-chapter="16">`), with no change to the build needed beyond this chat's. What the build asks of the chapter:

- `16-photography.json` in `work/build/guide/chapters/`, the shape of `17-motion-and-states.json`; `opener` is optional.
- Every rule needs a `failure` block, or the build warns ("the rule has no 'failure' block") and `--strict` fails.
- Each specimen `work/build/guide/specimens/s-16-*.html` has an entry in `manifest-photography.json` with `chapter`, `rule`, `alt` (15 characters or more), and `width_px` (a number for a fixed plate, or null for one that flows), plus `illustrative: true` where it shows an illustrative item.
- Photographs only by contract C1. A placeholder plate is ordinary HTML and CSS from the tokens.
- The weight: every build now notes "chapter 16: weighs N bytes against its allocation of 300,000 (P percent)". The photographs count in the page's "photographs" part, never in chapter 16.

### C3. The application kit (for chapters 20 to 25's builders)

Live since 02:24 UTC. `node work/build/app-kit/oa-app.mjs build [ID...] [--all] [--out DIR] [--exports DIR] [--no-export]`, run under the build lock.

- **A content file** per application, `work/build/app-kit/specs/<id>-<name>.json`: `id` (A01 on), `type` (a renderer's name), `platform` (a row id in `work/research/20261121_Platform-Specifications.json`, which sets the size and the safe area), `export_name` (the dated file name's words), the words, `alt`, `plate_head` and `plate_line`. Each renderer's header names the keys it reads.
- **A renderer** per type, `renderers/<type>.mjs`, exports `render(spec)` returning `{ w, h, html, css, layers, alt, exports, plate, live }`, static markup at true size, colors and type only by token (the build lists any token `tokens.css` lacks). Today: `social-post`, `web-page`, `report-page`. Shared parts in `lib.mjs`: `type_css(name)`, `mark(master)` (an identity master inlined with its paint variables), `frame()`, `plate()`, `overlay()` (named layers), `export_page()`, `fluid_cqi()`, `platform()`, `safe_boxes()`.
- **Reuse, never copy:** chapter 18's components by reading their files (`component_css()`); the chart kit's figures by its own `run_spec` and `K.figure`; the guide's sprite by `tools/sprite_symbols.py`.
- **Exports** go to `work/build/exports/phase-4/` with `<date>_Phase-4-Exports-Manifest.json`; `python3 -I work/build/app-kit/check-dimensions.py` checks them against the table, and `python3 -I work/build/app-kit/tools/export_checks.py <out> <exports>` reads their pixels.
- **A plate** is `out/<id>/plate.html`: the drawing at true size in an SVG `viewBox` frame (markup in `foreignObject`), its overlay switched on by a checkbox with scripts off. A web page's frames lay out by container queries and `cqi` type, so its CSS must not use media queries or `vw` for layout.

## Routine calls

- D4-xxx | Each photograph is drawn through CSS content replacement on its own `<img>` (`img[data-oa-photo="<name>"]{content:url(data:...)}` in one head style), not through SVG `<use>` | The SVG route resampled the photograph (softer at 1x; mean 2 to 4 levels off `<img>` in Chromium, even with `image-rendering` hints), so chapter 01 would have changed on screen; content replacement keeps the `<img>`, its alt and crop, and matched pixel for pixel; MDN's data gives it from Chrome 28, Firefox 63 and Safari 9
- D4-xxx | The photographs weigh as their own part of the page, "photographs", with a 0.5 MB figure, outside every chapter | They are carried once for the page and shown by chapters 01 and 16, so charging them to either chapter would misstate both; chapter 16's 300,000 already assumed them free
- D4-xxx | Chapter 01's three plates keep their tags as they were except the `src`, which gives way to `data-oa-photo` (the 1200 x 720 size hint and `loading` stay) | The fewest changes to approved plates; the captures prove nothing moved
- D4-xxx | A tight crop (`data-oa-crop`) is a frame the build writes around the `<img>`, placing the photograph by percent | `object-view-box` is Chromium only; percent placement works in every browser and keeps the crop at every width
- D4-xxx | G3-05: the edge guard in `checks.js` now holds every haloed word of every chart (the `t.clear_edges` gate is gone), and the fan chart's `labels.values_clear_edges` is on unless a spec sets it false | "Switch it on for every chart" covers both the test and the one form whose key moves a value; S59 is the only fan chart and already set it, so no drawing changes
- D4-xxx | Phase 4's seven chapters join `guide_charts.IN_PROGRESS`, so a chapter in place counts at its bytes or its allocation, whichever is more, until Gate 4 | Each is built across chats; a half-built chapter at its bytes alone would hand the rest of its allocation to the page's room
- D4-xxx | `guide_check.js` gains `photoDrawn` (every photograph request draws its copy) with one self-test plant | The build proves one copy; only a browser proves the CSS draws it
- D4-xxx | The projection past the 15.5 MB line prints as a note marked "early warning" and no longer fails a strict build; the line stays at 15.5 MB, and only the page past 16 MB stops a build | The Gate 3 report Dustin approved, section 9 ("the build reports and does not stop on", DR-271); the main session's answer at 02:08
- D4-xxx | The page's own size past 15.5 MB (`guide_build.py`'s `weigh()`) became the same early-warning note | The main session's rule that only the page itself past 16 MB fails; today's page is 12.23 MB, so nothing reads differently now
- D4-xxx | The report sample's PDF keeps the font types Chromium writes (Inter as Type 3, Inter Tight as CID TrueType); a "Not fixed" row hands the print fonts to chapter 25's preflight | The main session's answer at 02:08; nothing installed
- D4-xxx | The application kit lives in `work/build/app-kit/` on the chart kit's pattern: content files in `specs/`, one renderer per type in `renderers/`, one command (`oa-app.mjs build`), checks in `check-dimensions.py` and `tools/export_checks.py` | The brief's section 9 and the chart kit's layout
- D4-xxx | A plate draws its application at true size inside an SVG `viewBox` with the markup in `foreignObject`, so the frame scales it to the column with no script; the overlay draws in the same coordinates and a native checkbox shows it through `:has()` | Static markup (G3-07), keyboard and scripts-off both proved in Chromium
- D4-xxx | The web sample lays out by container queries on its own root and restates the seven fluid type tokens in `cqi`, read from `tokens.css`; its root resets to `1rem` and its landmarks set their own box properties | So each frame lays out as the page does alone at that width: an iframe per frame would carry the fonts again, and `vw` and a host page's `main {}` rule reached inside the frames until these went in
- D4-xxx | S86 in the article is drawn by the kit's own `run_spec` and `K.figure` at 621 and 328 px, and the drawings are set into the figure after `K.figure` | The narrowest column each drawing serves, so a drawing only scales up and no word drops under 13 px; `K.figure` holds phrases with HTML spans inside the SVG text, which ends the SVG when parsed ("Not fixed")
- D4-xxx | The kicker's CL-031 is drawn by `guide_build.Sprites` through `tools/sprite_symbols.py`, and chapter 18's theme switch by reading its own three files | Reuse, never copy (Gate 3 report section 9)
- D4-xxx | The sign-off is drawn from the 48 px master file with the social card's paint rule (links take the nodes' color on a dark ground) | The social card holds its paint inside its draw function, where nothing else can call it; the master is the source the card's copy came from
- D4-xxx | Re-sized Phase 4 allocations: 16 300,000; 20 757,000; 21 655,000; 22 277,000; 23 743,000; 24 338,000; 25 214,000; 3,284,000 in all | Measured plates times what section 9 says each chapter draws (`20261121_Phase-4-Allocations.md`); Gate 3's figures stay in the code as `PHASE_4_GATE_3`
- D4-xxx | The census entry numbers in the sample spec read zero-based (entry 41 is "Executive summary") | Checked against the file; every word the report sample prints matches its entry

## Done

Job 1, finished 02:02 UTC.

| Item | What changed | Files | Proof |
|---|---|---|---|
| 2, P4-5: each photograph once for the page | A specimen asks for a photograph by name, `<img data-oa-photo="<name>">` with no `src` (contract C1). The build checks each request (a known name, an alt, no `src`, a crop inside the photograph), turns a `data-oa-crop` request into its frame, warns on any photograph placed by its path, writes one rule per named photograph into `<style id="oa-photos">` in the head, and warns if any photograph's data sits in the page more than once. The photographs weigh as their own part, "photographs" (0.5 MB figure). The build report gains `photographs`: each one's uses, plates and copies. Chapter 01's three plates ask by name; only their `src` changed | New `work/build/scripts/phase-4/guide_photos.py` (registry `PHOTOS`, `photo_img()`, `photo_style()`, `expand()`, self-test); `work/build/scripts/phase-2/guide_build.py` (import, `process_fragment`, `place_photos()`, `weigh()`, `WEIGHT_FIXED`, report, one self-test scenario); `work/build/scripts/phase-2/guide_editor_ch01.py` (`PHOTO_NAME`, the `ph` tag); outputs `s-01-6-correct.html`, `s-01-8-correct.html`, `s-01-8-failure.html`; `work/build/scripts/phase-2/guide_check.js` (`photoDrawn` and its plant) | Chapter 01's chain (`guide_editor_build.py`, then `stage_b_identity_ch01.py`) rerun under the lock: of every file under `work/build/guide/`, only those three plates changed, each by its `src` alone. **Bytes freed: 190,804** (strict page 12,210,920 to 12,020,116 on the same inputs; chapter 01 1,356,074 to 675,807; the new photographs part 489,462; head 1 byte more). Captures of Rules 01.6 and 01.8, whole rule blocks and all four plates, at 1440, 1024, 390 and 360 px at 1x and at 1440 and 390 px at 2x: **36 of 36 identical, pixel for pixel**, before and after |
| 1, G3-05: label clearance on for every chart | The edge guard (DD-E1) in `checks.js` holds every haloed word of every chart; the `t.clear_edges` gate is gone. The fan chart's `labels.values_clear_edges` is on unless a spec sets it false | `work/build/chart-kit/checks.js`, `work/build/chart-kit/forms/fan-chart.js` (header and one line) | Kit `build --all --no-png` (sweep included) before and after, under the lock: **96 of 96 PASS both times; all 192 files it writes (96 CSV exports, 96 check files) hash the same.** That run writes no SVG (its own last line says "no PNG, SVG or captures"), so I also hashed every drawing the SVG exports are drawn from, by the kit's own `run_spec` (each spec at 1440 and 390 px on Newsprint and Charcoal, S95's crops, the card forms' HTML): **368 SVG drawings and 8 card HTML outputs, all the same; 0 faults before and after.** `plate-share.json` unchanged. Hashes and logs: `.../scratchpad/c10/engineer/g305/` |
| 3, the weight projection | Phase 4's seven chapters take the Gate 3 report's allocations (16: 300,000; 20: 500,000; 21: 460,000; 22: 300,000; 23: 660,000; 24: 450,000; 25: 340,000; 3,010,000 in all) in place of 362,857 each. Each built Phase 4 chapter is reported against its own figure on every build ("chapter 16: weighs N bytes against its allocation of 300,000 (P percent)"), recorded in `projection.phase_4_built`, and held to its allocation in the projection while built. The ST-S10 note lists each figure and their sum | `work/build/scripts/phase-3/guide_charts.py` (`PHASE_4_ALLOCATION`, `ALLOCATION`, `IN_PROGRESS`, `gates()`, self-test); `guide_build.py` (`weigh()` leaves Phase 4 chapters to `guide_charts` and gives each its allocation as its budget) | `guide_charts.py --self-test`: 34 pass, every planted fault caught, two new (the seven figures; a built chapter under and one byte over). Strict build: **projection 15,460,028 bytes** (12,020,117 today plus 3,010,000 plus chapter 15's 29,899 held), 539,972 under 16 MB and 39,972 under the 15.5 MB warning. Without this chat's 190,804 bytes freed it would sit 150,832 past 15.5 MB, as the Gate 3 report foresaw |
| 4, chapter 16's place in the build | Nothing more needed: contract C2 | (none beyond the above) | A fixture chapter 16 built strictly into copies of today's chapters and specimens: placed under Evidence and media, reported at 10,499 of 300,000 bytes; the photographs carried once with five uses across chapters 01 and 16; the only warning was the fixture's own missing failure plate. The build's self-test now holds a chapter 16 scenario |

Job 2, the application kit, finished 02:27 UTC.

| Part | What it is | Files | Proof |
|---|---|---|---|
| The kit | One command draws each application from its content file at build time into static markup, with the guide's tokens and fonts: `node work/build/app-kit/oa-app.mjs build --all`. It writes each standalone export page and the facts the checks read to scratch, the exports to `work/build/exports/phase-4/` with a dated manifest, each plate, and a measurement page | `work/build/app-kit/oa-app.mjs`, `lib.mjs`, `renderers/social-post.mjs`, `renderers/web-page.mjs`, `renderers/report-page.mjs`, `specs/a01-instagram-portrait.json`, `specs/a02-web-article.json`, `specs/a03-report-page.json`, `tools/sprite_symbols.py`, `tools/pdf_boxes.py` | Every token the renderers name is in `tokens.css` (the build checks); the three samples drawn as the sample spec's sections 1 to 3 set them, looked at full size |
| Exports | 11 files: the post PNG 1080 by 1350; the article as full-page PNGs at 1440, 1024, 390 and 360 px, light and dark; the report page as a PDF (630 by 810 pt media and bleed box, trim box 9, 9, 621, 801 pt, tagged, titled) and its 840 by 1080 proof PNG | `work/build/exports/phase-4/20261121_*` and `20261121_Phase-4-Exports-Manifest.json` | `check-dimensions.py`: **11 of 11 pass** against the research lead's table |
| Plates | Each sample at true size in a frame that scales it, with its safe-area overlay switched on by a native checkbox | (in scratch: `app-out/<id>/plate.html`, `app-out/measure.html`) | Chromium: the overlay shows after Tab and Space, with scripts on and off; each of the eight article frames lays out as the export at its width (columns 867, 783, 350 and 328 px; titles 110, 88.6, 56 and 56 px; headline breaks exactly as spec 2.7 lists) |
| Checks on the exports' pixels | `tools/export_checks.py`: words and marks inside the live box (by their ink), the post's 36 px floor, one working red, contrast word by word on the pixels, Newsprint, Charcoal and red shares, the post's feed test | `work/build/app-kit/tools/export_checks.py` | **8 of 10 views pass.** The two that do not: the article's light captures at 1440 (88.2 percent Newsprint) and 1024 (85.9), past Rule 05.1's 85 (Requests) |
| Web checks | axe (the guide check's library) at every width and theme; Tab order; the theme kept after a reload; reflow at 320 px; text at 200 percent | in `oa-app.mjs` | axe **0 violations** at all 8; Tab reaches the skip link, home, the checked theme and the figure's table, each with a 2 px ring; Dark chosen, reloaded, still Dark (and Light); nothing wider than the window at 320 px or at 200 percent |
| Measure | The three plates placed in a copy of today's guide and read back with their frames: **post 11,696; article at 4 widths and 2 themes 187,145; report page 11,355** | `work/handoffs/phase-4/20261121_Phase-4-Allocations.md` | Two fixture builds, base and with, in the same mode; the sprite unchanged (CL-031 is already in it) |
| Allocations | Re-sized from the measures by counting what each chapter draws: 3,284,000 in all (Gate 3: 3,010,000); set in `guide_charts.py` | `work/build/scripts/phase-3/guide_charts.py` | Strict build at 02:24 with chapter 16 in place: exit 0, 0 warnings, 12,233,841 bytes; projection 15,734,059, 265,941 under 16 MB, printed as the early warning; `guide_charts.py --self-test` 34 pass; `guide_build.py --self-test` 39 of 39 |
| The 15.5 MB line | A note marked "early warning", never a failure; the page past 16 MB still stops | `guide_charts.py` (`gates()`, its self-test case), `guide_build.py` (`weigh()`) | Both self-tests above; the strict build prints the note and exits 0 |

**Contrast, measured on the exports' pixels** (ink on ground, WCAG ratio; Master Brief section 22 wants 4.5 for text, 3 for large text and marks):

| Pair | Where | Ratio |
|---|---|---|
| Charcoal #121212 on Newsprint #DCD9D2 | every light export's text | 13.29 |
| Deep Stone #4E535B on Newsprint | the post's kicker tail, the article's and the report's secondary words | 5.49 |
| Dim Newsprint #A3A19C on Charcoal | the post's source line, the dark article's secondary words, the footer note | 7.26 |
| Newsprint on Charcoal | the dark article's text, the footer | 13.29 |
| White on Charcoal | S86's label inside its Charcoal circle (light theme) | 18.73 |
| Ampersand B, Pillar Red #E63946 on Newsprint | the post's headline (a mark, named "and") | 2.96, as the design director's table expects; the design director's notes hold it for the accessibility review |
| Lockmark lever, Pillar Red on Charcoal | the post's sign-off | 4.49 |
| Lockmark nodes, Newsprint on Charcoal | the post's sign-off | 13.29 |

The post's feed test (Rule 08.2, dark card): reduced to 432 px, 8 of 8 nodes keep a light 2 by 2 block and the lever 36 red pixels; at 360 px, 8 of 8 and 32. Newsprint covers 66.2 percent of the post (the design director's prototype: 66.3), red 0.22 percent.

**The report PDF's fonts** (`pdffonts`, which is installed here at `/usr/bin/pdffonts`): Inter as **Type 3**, four subsets all named Inter-Regular (Chromium instances the variable font at 400, 600 and 700 and writes each as Type 3), embedded and subset; Inter Tight ExtraBold as **CID TrueType** (Identity-H), embedded and subset. See "Not fixed".

Closing, 02:00 to 02:02 UTC: strict build exit 0, 0 warnings, 12,020,117 bytes, 369 rules, 679 specimens (the chart kit part 1 byte more, from `fan-chart.js`); `guide_build.py --self-test` 39 of 39 scenarios, 395 of 395 expectations; `phase3_ch14_build.py --check` 99 of 99; kit 96 of 96.

## Requests

- **Answered at 02:08 UTC (option b; see Routine calls and Not fixed).** Main session, for a decision (02:06 UTC): the permission check refused `pip install brotli` (auto mode classifier, "Undermining Oversight"). I did not route around it. Why I asked: the report page's PDF (sample spec 3.4) must embed Inter as TrueType, since the design director's test print found Chromium writing the variable Inter as Type 3, which some print workflows reject; the fix the spec names is static instances of Inter 400, 600 and 700, and fontTools needs the `brotli` package to read the guide's WOFF2 files to make them. Options: (a) allow the install (one small package from PyPI, into the container, nothing in the repository); (b) build the report sample with whatever Chromium writes and list Inter's font type in the preflight as not fixed, leaving it to chapter 25's print preflight; (c) another owner supplies static Inter TTF instances made elsewhere. Nothing else in Job 2 depends on it: the social post, the web article, the dimension script and the measurement can go ahead on resume.
- Main session: run `guide_check.js --self-test` on the joined build. It gains one plant (`photoDrawn`); I proved its expression with a probe on my page (3 requests drawn, 0 undrawn; the plant caught), not by running the check.
- Main session: the projection now sits 39,972 bytes under the 15.5 MB warning. The warning fails a strict build, so once Job 2 re-sizes the allocations upward (chapters 20 and 23 draw more than their nearest chapters), the strict build will warn until the 15.5 MB line is raised or the figures move. I will report the re-sized projection in the allocations file and leave the line where it is.

- Design director: the article sample's light captures cover 88.2 percent Newsprint at 1440 px and 85.9 at 1024, past Rule 05.1's 60 to 85 that spec 2.7 asks of them (390 and 360 px measure 81.5 and 81.0). The page is the spec's page as written; the fix is a design call (a Charcoal or Prussian panel, or a wider footer), so I left it. Measured by `tools/export_checks.py` on the exports.
- Design director and chapter 20's builder: placed in the guide as a plate, the article frames hold 16 headings (h1, h2 and the figure's own), which the guide's heading rule warns on inside a specimen, and chapter 18's switch markup inlines the Selected check path, which the build warns on from chapter 09 (draw it from the sprite). The report page holds 4 headings. Neither touches this chat's measures; each is a choice for the chapter that places them (an image stage, or a plate kind that allows headings, as chapter 14's selection guide does).
- Main session: the fonts note in your 02:08 message said `pdffonts` is not installed; it is, at `/usr/bin/pdffonts`, and I used it.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| NF-E1 | Engineer, chat 10, Job 2 | `work/build/exports/phase-4/20261121_Studio-Sample-Report-Page-03-Letter.pdf`; the kit's PDF path in `work/build/app-kit/oa-app.mjs` | Chromium writes the variable Inter as Type 3 fonts (four subsets, named Inter-Regular), which some print workflows reject; Inter Tight comes out as CID TrueType. Print PDFs need embedded TrueType or CFF fonts | Settle in chapter 25's print preflight (chat 15): embed static Inter instances. Static Inter 4.000 OTF files are installed on this system at `/usr/share/fonts/opentype/inter/` (Inter only; no static Inter Tight or Lora), which may serve chat 15 without `brotli`; making static instances from the guide's WOFF2 files needs `brotli` for fontTools | The main session's answer (02:08): accept Chromium's types for this measurement sample and install nothing; the install question goes to Dustin for chat 15 | Open, chat 15 |
| NF-E2 | Engineer, chat 10, Job 2 | `work/build/chart-kit/kit-build.js`, `K.figure` and `K.hold`; the kit's lean method (`oa-chart.mjs fragments` with `method: lean`) | `K.figure` holds phrases together with HTML `<span class="oac-nw">` across the whole figure, `opts.svg` included, so a lean figure's SVG text gets an HTML span, which ends the SVG when the page is parsed (S86's "this scale." printed outside its drawing). The guide uses `load-table`, which puts no SVG in the figure, so no reader has seen it | Hold phrases outside `opts.svg` only, or as SVG `tspan`s inside it; prove the guide's page and the kit's exports unchanged | The application kit works around it (the drawings go in after `K.figure`); a kit change was outside this chat's job and needs its own proof | Open |

## Tested

- Job 1 (01:40 to 02:02 UTC), each in its row under Done: chapter 01's generator chain with hashes of every guide output; the strict build before and after; 36 Chromium captures compared pixel for pixel; a prototype of three other routes (SVG `<use>`, CSS background, `image-rendering` hints), measured against `<img>`, rejected; MDN's compatibility data for content replacement (read, not run in other browsers); `guide_photos.py --self-test` 9 of 9; a chapter 16 fixture build; the kit's whole build and every drawing hashed before and after G3-05; `guide_charts.py --self-test`; `guide_build.py --self-test`; `phase3_ch14_build.py --check`; a probe of `photoDrawn`.
- `check-dimensions.py --self-test` (Job 2's script): an exact PNG, one a pixel short, a free height, a minimum, a PDF with bleed and trim boxes, one without, a missing file and an unknown row, each judged right.
- Job 2 (02:08 to 02:27 UTC), each in its row under Done: the kit's build (three samples, 11 exports); `check-dimensions.py` 11 of 11 and its self-test; `tools/export_checks.py` on every PNG (live box by ink, floor, reds, contrast word by word, shares, the feed test); axe, Tab order, the theme after reload, reflow at 320 px and 200 percent text on the article at every width and theme; the measurement page in Chromium at 1440 and 390 px (frames, overlay by keyboard, scripts off); two fixture builds for the placed bytes; `pdffonts` and `pdfinfo -box` on the PDF; `guide_charts.py --self-test`; `guide_build.py --self-test`; the strict build with chapter 16 in place. I looked at the post, the article at 1440 light and 390 dark, the report proof, and the plates with their overlays.

## Not tested

- The application kit's exports in any browser but Chromium; the email-like dark mode of a mail app (no email this chat).
- The article's keyboard walk beyond the first eight Tab stops (the figure's table opened and read), and a screen reader on any sample.
- "No clipped box" at 200 percent text: I tested only that nothing runs wider than the window.
- The report PDF in a print workflow or preflight tool; its reading order (tagged, but the tag tree not read).
- The plates inside the guide's real shell with its fit switch (they do not go into the guide this chat); their placed bytes come from a fixture build of today's guide.
- The `guide_check.js` red, party and label tests on the samples (the main session's closing checks run the guide check on the guide, which does not hold them).
- Content replacement in Firefox and Safari: only Chromium is installed here. MDN's data lists it from Firefox 63 and Safari 9; Safari, Firefox and real screen readers stay on Gate 4's list (DR-279).
- The guide check (`guide_check.js`) itself, its self-test included: the main session runs it.
- The photographs in print emulation and forced colors (content replacement is not a background, so neither should drop it; not looked at).
- A full kit `build --all` with PNG and SVG files: G3-05's SVGs were proved by hashing every drawing they are made from, in Node.
