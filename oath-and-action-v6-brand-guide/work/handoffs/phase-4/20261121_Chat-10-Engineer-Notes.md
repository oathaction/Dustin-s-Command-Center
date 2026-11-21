# Chat 10: engineer notes

Status: 01:45 UTC. Started 01:36 UTC. Job 1 item 2's contract written first (C1 below, revised 01:45 UTC); building it now.

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

Proved at 01:57 UTC with a fixture chapter 16 (two rules, three plates, two photograph requests) built strictly into a copy of today's chapters: the page puts `16-photography.json` in place of the placeholder, under Evidence and media (`<section class="chapter chapter--grouped" id="photography" data-part="evidence" data-chapter="16">`), with no change to the build needed beyond this chat's. What the build asks of the chapter:

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

## Requests

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

## Not tested
