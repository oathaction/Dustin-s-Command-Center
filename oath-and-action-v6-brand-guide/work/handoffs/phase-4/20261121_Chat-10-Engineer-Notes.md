# Chat 10: engineer notes

Status: 02:07 UTC. Started 01:36 UTC. Job 1 done (all four items). Job 2 started, then **stopped at 02:06 UTC on a refused permission** (Requests, first item); handed back to the main session as the brief asks.

**Job 1 summary (02:03 UTC), for the main session:**
1. P4-5: photographs drawn by name from one copy per page (contract C1), by CSS content replacement on each `<img>`; chapter 01's three plates changed only their `src`.
2. 190,804 bytes freed (12,210,920 to 12,020,116); chapter 01 675,807; new "photographs" part 489,462.
3. Rules 01.6 and 01.8: 36 of 36 captures pixel-identical (1440, 1024, 390, 360 px at 1x; 1440 and 390 at 2x).
4. G3-05: the edge guard holds every word of every chart, and the fan chart's key is on by default; kit 96 of 96, all 192 written files and all 376 drawings hash the same before and after.
5. Projection: Phase 4's seven allocations (3,010,000) in `guide_charts.py`; each built Phase 4 chapter reported against its own; projection 15,460,028, 39,972 under 15.5 MB.
6. Chapter 16 builds in place with no further change (contract C2, proved on a fixture).
7. Closing: strict exit 0, 0 warnings, 12,020,117 bytes; build self-test 39 of 39; chapter 14 check 99 of 99. The guide check's new `photoDrawn` is yours to run.
Job 2 is under way: the sample specs and the specifications JSON are both in.

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

## Routine calls

- D4-xxx | Each photograph is drawn through CSS content replacement on its own `<img>` (`img[data-oa-photo="<name>"]{content:url(data:...)}` in one head style), not through SVG `<use>` | The SVG route resampled the photograph (softer at 1x; mean 2 to 4 levels off `<img>` in Chromium, even with `image-rendering` hints), so chapter 01 would have changed on screen; content replacement keeps the `<img>`, its alt and crop, and matched pixel for pixel; MDN's data gives it from Chrome 28, Firefox 63 and Safari 9
- D4-xxx | The photographs weigh as their own part of the page, "photographs", with a 0.5 MB figure, outside every chapter | They are carried once for the page and shown by chapters 01 and 16, so charging them to either chapter would misstate both; chapter 16's 300,000 already assumed them free
- D4-xxx | Chapter 01's three plates keep their tags as they were except the `src`, which gives way to `data-oa-photo` (the 1200 x 720 size hint and `loading` stay) | The fewest changes to approved plates; the captures prove nothing moved
- D4-xxx | A tight crop (`data-oa-crop`) is a frame the build writes around the `<img>`, placing the photograph by percent | `object-view-box` is Chromium only; percent placement works in every browser and keeps the crop at every width
- D4-xxx | G3-05: the edge guard in `checks.js` now holds every haloed word of every chart (the `t.clear_edges` gate is gone), and the fan chart's `labels.values_clear_edges` is on unless a spec sets it false | "Switch it on for every chart" covers both the test and the one form whose key moves a value; S59 is the only fan chart and already set it, so no drawing changes
- D4-xxx | Phase 4's seven chapters join `guide_charts.IN_PROGRESS`, so a chapter in place counts at its bytes or its allocation, whichever is more, until Gate 4 | Each is built across chats; a half-built chapter at its bytes alone would hand the rest of its allocation to the page's room
- D4-xxx | `guide_check.js` gains `photoDrawn` (every photograph request draws its copy) with one self-test plant | The build proves one copy; only a browser proves the CSS draws it

## Done

Job 1, finished 02:02 UTC.

| Item | What changed | Files | Proof |
|---|---|---|---|
| 2, P4-5: each photograph once for the page | A specimen asks for a photograph by name, `<img data-oa-photo="<name>">` with no `src` (contract C1). The build checks each request (a known name, an alt, no `src`, a crop inside the photograph), turns a `data-oa-crop` request into its frame, warns on any photograph placed by its path, writes one rule per named photograph into `<style id="oa-photos">` in the head, and warns if any photograph's data sits in the page more than once. The photographs weigh as their own part, "photographs" (0.5 MB figure). The build report gains `photographs`: each one's uses, plates and copies. Chapter 01's three plates ask by name; only their `src` changed | New `work/build/scripts/phase-4/guide_photos.py` (registry `PHOTOS`, `photo_img()`, `photo_style()`, `expand()`, self-test); `work/build/scripts/phase-2/guide_build.py` (import, `process_fragment`, `place_photos()`, `weigh()`, `WEIGHT_FIXED`, report, one self-test scenario); `work/build/scripts/phase-2/guide_editor_ch01.py` (`PHOTO_NAME`, the `ph` tag); outputs `s-01-6-correct.html`, `s-01-8-correct.html`, `s-01-8-failure.html`; `work/build/scripts/phase-2/guide_check.js` (`photoDrawn` and its plant) | Chapter 01's chain (`guide_editor_build.py`, then `stage_b_identity_ch01.py`) rerun under the lock: of every file under `work/build/guide/`, only those three plates changed, each by its `src` alone. **Bytes freed: 190,804** (strict page 12,210,920 to 12,020,116 on the same inputs; chapter 01 1,356,074 to 675,807; the new photographs part 489,462; head 1 byte more). Captures of Rules 01.6 and 01.8, whole rule blocks and all four plates, at 1440, 1024, 390 and 360 px at 1x and at 1440 and 390 px at 2x: **36 of 36 identical, pixel for pixel**, before and after |
| 1, G3-05: label clearance on for every chart | The edge guard (DD-E1) in `checks.js` holds every haloed word of every chart; the `t.clear_edges` gate is gone. The fan chart's `labels.values_clear_edges` is on unless a spec sets it false | `work/build/chart-kit/checks.js`, `work/build/chart-kit/forms/fan-chart.js` (header and one line) | Kit `build --all --no-png` (sweep included) before and after, under the lock: **96 of 96 PASS both times; all 192 files it writes (96 CSV exports, 96 check files) hash the same.** That run writes no SVG (its own last line says "no PNG, SVG or captures"), so I also hashed every drawing the SVG exports are drawn from, by the kit's own `run_spec` (each spec at 1440 and 390 px on Newsprint and Charcoal, S95's crops, the card forms' HTML): **368 SVG drawings and 8 card HTML outputs, all the same; 0 faults before and after.** `plate-share.json` unchanged. Hashes and logs: `.../scratchpad/c10/engineer/g305/` |
| 3, the weight projection | Phase 4's seven chapters take the Gate 3 report's allocations (16: 300,000; 20: 500,000; 21: 460,000; 22: 300,000; 23: 660,000; 24: 450,000; 25: 340,000; 3,010,000 in all) in place of 362,857 each. Each built Phase 4 chapter is reported against its own figure on every build ("chapter 16: weighs N bytes against its allocation of 300,000 (P percent)"), recorded in `projection.phase_4_built`, and held to its allocation in the projection while built. The ST-S10 note lists each figure and their sum | `work/build/scripts/phase-3/guide_charts.py` (`PHASE_4_ALLOCATION`, `ALLOCATION`, `IN_PROGRESS`, `gates()`, self-test); `guide_build.py` (`weigh()` leaves Phase 4 chapters to `guide_charts` and gives each its allocation as its budget) | `guide_charts.py --self-test`: 34 pass, every planted fault caught, two new (the seven figures; a built chapter under and one byte over). Strict build: **projection 15,460,028 bytes** (12,020,117 today plus 3,010,000 plus chapter 15's 29,899 held), 539,972 under 16 MB and 39,972 under the 15.5 MB warning. Without this chat's 190,804 bytes freed it would sit 150,832 past 15.5 MB, as the Gate 3 report foresaw |
| 4, chapter 16's place in the build | Nothing more needed: contract C2 | (none beyond the above) | A fixture chapter 16 built strictly into copies of today's chapters and specimens: placed under Evidence and media, reported at 10,499 of 300,000 bytes; the photographs carried once with five uses across chapters 01 and 16; the only warning was the fixture's own missing failure plate. The build's self-test now holds a chapter 16 scenario |

Job 2, the application kit, where it stood at 02:06 UTC:

| Part | State | File |
|---|---|---|
| Dimension script | Written and self-tested: PNG pixels (exact, at least, at most, ratio; a null side skipped), PDF trim, media and bleed boxes against the row's bleed, every font embedded, bytes under `max_bytes`; reads the newest `*_Phase-4-Exports-Manifest.json` in `work/build/exports/phase-4/` and the research lead's JSON; a pass or fail per file | `work/build/app-kit/check-dimensions.py` |
| Shared parts | Written, not yet run end to end: tokens and fonts for export pages, chapter 18's component CSS read from its own file, the platform rows, safe-area boxes from a row's `safe_area`, the plate (the drawing at true size in an SVG `viewBox` frame that scales it, an overlay in the same coordinates, switched on by a native checkbox and `:has()`, so keyboard and scripts off both work), the export page | `work/build/app-kit/lib.mjs` |
| Renderers, command, specs, exports, measurement, allocations file | Not started. The plan, from the sample spec: the web sample lays out with container queries on its own root and re-declares the fluid type tokens with `cqi` read from `tokens.css` (they use `vw`, which inside a guide frame would follow the guide's window; an iframe per width would carry the fonts again in every frame); S86 drawn by the kit's own `run_spec` and `K.figure` at 621 and 328 px, the smallest width each drawing serves, so no word drops under 13 px when it scales; the kicker's CL-031 from `guide_build.Sprites`, the guide's own sprite code; the sign-off from the 48 px master with the social card's paint rule; chapter 18's theme switch read from `c-18-theme-switch.html`, `.css` and `.js` | (next) |

Closing, 02:00 to 02:02 UTC: strict build exit 0, 0 warnings, 12,020,117 bytes, 369 rules, 679 specimens (the chart kit part 1 byte more, from `fan-chart.js`); `guide_build.py --self-test` 39 of 39 scenarios, 395 of 395 expectations; `phase3_ch14_build.py --check` 99 of 99; kit 96 of 96.

## Requests

- **Main session, for a decision (02:06 UTC): the permission check refused `pip install brotli`** (auto mode classifier, "Undermining Oversight"). I did not route around it. Why I asked: the report page's PDF (sample spec 3.4) must embed Inter as TrueType, since the design director's test print found Chromium writing the variable Inter as Type 3, which some print workflows reject; the fix the spec names is static instances of Inter 400, 600 and 700, and fontTools needs the `brotli` package to read the guide's WOFF2 files to make them. Options: (a) allow the install (one small package from PyPI, into the container, nothing in the repository); (b) build the report sample with whatever Chromium writes and list Inter's font type in the preflight as not fixed, leaving it to chapter 25's print preflight; (c) another owner supplies static Inter TTF instances made elsewhere. Nothing else in Job 2 depends on it: the social post, the web article, the dimension script and the measurement can go ahead on resume.
- Main session: run `guide_check.js --self-test` on the joined build. It gains one plant (`photoDrawn`); I proved its expression with a probe on my page (3 requests drawn, 0 undrawn; the plant caught), not by running the check.
- Main session: the projection now sits 39,972 bytes under the 15.5 MB warning. The warning fails a strict build, so once Job 2 re-sizes the allocations upward (chapters 20 and 23 draw more than their nearest chapters), the strict build will warn until the 15.5 MB line is raised or the figures move. I will report the re-sized projection in the allocations file and leave the line where it is.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

- Job 1 (01:40 to 02:02 UTC), each in its row under Done: chapter 01's generator chain with hashes of every guide output; the strict build before and after; 36 Chromium captures compared pixel for pixel; a prototype of three other routes (SVG `<use>`, CSS background, `image-rendering` hints), measured against `<img>`, rejected; MDN's compatibility data for content replacement (read, not run in other browsers); `guide_photos.py --self-test` 9 of 9; a chapter 16 fixture build; the kit's whole build and every drawing hashed before and after G3-05; `guide_charts.py --self-test`; `guide_build.py --self-test`; `phase3_ch14_build.py --check`; a probe of `photoDrawn`.
- `check-dimensions.py --self-test` (Job 2's script): an exact PNG, one a pixel short, a free height, a minimum, a PDF with bleed and trim boxes, one without, a missing file and an unknown row, each judged right.

## Not tested

- Job 2's renderers, exports, safe-area and contrast checks, and the measurement: not started when the permission stop came.
- Content replacement in Firefox and Safari: only Chromium is installed here. MDN's data lists it from Firefox 63 and Safari 9; Safari, Firefox and real screen readers stay on Gate 4's list (DR-279).
- The guide check (`guide_check.js`) itself, its self-test included: the main session runs it.
- The photographs in print emulation and forced colors (content replacement is not a background, so neither should drop it; not looked at).
- A full kit `build --all` with PNG and SVG files: G3-05's SVGs were proved by hashing every drawing they are made from, in Node.
